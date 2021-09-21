import time
import pandas as pd
from tqdm import tqdm
from cassandra.cluster import Cluster

file_path = "~/Downloads/fma_dataset.csv"
dataset = pd.read_csv(file_path)

cluster = Cluster(['localhost'])
session = cluster.connect('music')

session.execute(
    'DROP TABLE IF EXISTS Q10')

session.execute(
    'CREATE TABLE IF NOT EXISTS Q10 (' +
    'title_album text, track_id int, title_track text, year_released int, month_released int, day_released int,' + 
    'artist text, duration int, genre text, favorites_artist int, listens_track int,' +
    'favorites_track int, listens_album int, favorites_album int,' +
    'PRIMARY KEY(year_released, listens_album, track_id))' +
    'WITH CLUSTERING ORDER BY (listens_album DESC);')


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
    insert_query = "INSERT INTO Q10(title_album, track_id, title_track, year_released, month_released, day_released," + \
        "artist, duration, genre, favorites_artist, listens_track," + \
        "favorites_track, listens_album, favorites_album) VALUES" + \
        "(\'{}\',{},\'{}\',{},{},{},\'{}\',{},\'{}\',{},{},{},{},{})".format(
        title_album, track_id, title_track, year_released, month_released, day_released, 
        artist, duration, genre, favorites_artist, listens_track,
        favorites_track, listens_album, favorites_album)
    session.execute(insert_query)
print("Data adding time: {} s".format(time.time() - start_time))

start_time = time.time()
rows = session.execute('SELECT artist, listens_album, year_released FROM Q10 WHERE year_released in (2015, 2016, 2017) ' + 
    'GROUP BY year_released PER PARTITION LIMIT 1')
print("Query time: {} s".format(time.time() - start_time))
seen_artists = set()
print("Results:")
for row in rows:
    if row.artist not in seen_artists:
        print("Artist: {}, Album Listened: {}, Year: {}".format(row.artist, row.listens_album, row.year_released))
        seen_artists.add(row.artist)
