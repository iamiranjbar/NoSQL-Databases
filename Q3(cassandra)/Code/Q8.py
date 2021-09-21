import time
import pandas as pd
from tqdm import tqdm
from cassandra.cluster import Cluster

file_path = "~/Downloads/fma_dataset.csv"
dataset = pd.read_csv(file_path)

cluster = Cluster(['localhost'])
session = cluster.connect('music')

session.execute(
    'DROP TABLE IF EXISTS Q8')

session.execute(
    'CREATE TABLE IF NOT EXISTS Q8 (' +
    'title_album text, track_id int, title_track text, year_released int, month_released int, day_released int,' + 
    'artist text, duration int, genre text, favorites_artist int, listens_track int,' +
    'favorites_track int, listens_album int, favorites_album int,' +
    'PRIMARY KEY((year_released, genre), favorites_album, track_id))' +
    'WITH CLUSTERING ORDER BY (favorites_album DESC);')


start_time = time.time()
for _, row in tqdm(dataset.iterrows(), total=dataset.shape[0]):
    title_album = row["title_album"].replace("'","''") if not isinstance(row["title_album"], float)   else ""
    track_id = row["track_id"]
    title_track = row["title_track"].replace("'","''") if not isinstance(row["title_track"], float) else ""
    year_released, month_released, day_released = [int(x) for x in row["date_released"].split(' ')[0].split('-')] if not isinstance(row["date_released"], float) else [0,0,0]
    artist = row["artist"].replace("'","''") if not isinstance(row["artist"], float) else ""
    duration = row["duration"]
    genre = row["genre"].replace("'","''") if not isinstance(row["genre"], float) else ""
    favorites_artist = row["favorites_artist"]
    listens_track = row["listens_track"]
    favorites_track = row["favorites_track"]
    listens_album = row["listens_album"]
    favorites_album = row["favorites_album"]
    insert_query = "INSERT INTO Q8(title_album, track_id, title_track, year_released, month_released, day_released," + \
        "artist, duration, genre, favorites_artist, listens_track," + \
        "favorites_track, listens_album, favorites_album) VALUES" + \
        "(\'{}\',{},\'{}\',{},{},{},\'{}\',{},\'{}\',{},{},{},{},{})".format(
        title_album, track_id, title_track, year_released, month_released, day_released, 
        artist, duration, genre, favorites_artist, listens_track,
        favorites_track, listens_album, favorites_album)
    session.execute(insert_query)
print("Data adding time: {} s".format(time.time() - start_time))

start_time = time.time()
rows = session.execute('SELECT title_album, favorites_album, favorites_artist FROM Q8 WHERE year_released=2016 AND genre = \'Rock\'')
print("Query time: {} s".format(time.time() - start_time))
seen_albums = set()
print("Results:")
for row in rows:
    if not row.title_album in seen_albums:
        print("Album: {}, Favorites Counts: {}, Album Artist Favorites: {}".format(row.title_album, row.favorites_album, row.favorites_artist))
        seen_albums.add(row.title_album)