import time
import pandas as pd
from tqdm import tqdm
from cassandra.cluster import Cluster

file_path = "~/Downloads/fma_dataset.csv"
dataset = pd.read_csv(file_path)

cluster = Cluster(['localhost'])
session = cluster.connect('music')

session.execute(
    'DROP TABLE IF EXISTS Q1')

session.execute(
    'CREATE TABLE IF NOT EXISTS Q1 (' +
    'title_album text, track_id int, title_track text, date_released text,' + 
    'artist text, duration int, genre text, favorites_artist int, listens_track int,' +
    'favorites_track int, listens_album int, favorites_album int,' +
    'PRIMARY KEY(title_album, track_id))')


start_time = time.time()
for _, row in tqdm(dataset.iterrows(), total=dataset.shape[0]):
    title_album = row["title_album"].replace("'","''") if not isinstance(row["title_album"], float)   else ""
    track_id = row["track_id"]
    title_track = row["title_track"].replace("'","''") if not isinstance(row["title_track"], float) else ""
    date_released = row["date_released"]
    artist = row["artist"].replace("'","''") if not isinstance(row["artist"], float) else ""
    duration = row["duration"]
    genre = row["genre"].replace("'","''") if not isinstance(row["genre"], float) else ""
    favorites_artist = row["favorites_artist"]
    listens_track = row["listens_track"]
    favorites_track = row["favorites_track"]
    listens_album = row["listens_album"]
    favorites_album = row["favorites_album"]
    insert_query = "INSERT INTO Q1(title_album, track_id, title_track, date_released," + \
        "artist, duration, genre, favorites_artist, listens_track," + \
        "favorites_track, listens_album, favorites_album) VALUES" + \
        "(\'{}\',{},\'{}\',\'{}\',\'{}\',{},\'{}\',{},{},{},{},{})".format(
        title_album, track_id, title_track, date_released, 
        artist, duration, genre, favorites_artist, listens_track,
        favorites_track, listens_album, favorites_album)
    if title_album == '':
        continue
    session.execute(insert_query)
print("Data adding time: {}s".format(time.time() - start_time))

start_time = time.time()
rows = session.execute('SELECT title_track FROM Q1 WHERE title_album = \'Rumble, Young Man, Rumble\'')
print("Query time: {}s".format(time.time() - start_time))
for row in rows:
    print(row.title_track)
