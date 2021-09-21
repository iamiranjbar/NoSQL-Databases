import time
import pandas as pd
from tqdm import tqdm
from cassandra.cluster import Cluster

file_path = "~/Downloads/fma_dataset.csv"
dataset = pd.read_csv(file_path)

cluster = Cluster(['localhost'])
session = cluster.connect('music')

session.execute(
    'DROP TABLE IF EXISTS Q91')

session.execute(
    'DROP TABLE IF EXISTS Q92')

session.execute(
    'DROP TABLE IF EXISTS Q93')

session.execute(
    'CREATE TABLE IF NOT EXISTS Q91 (' +
    'title_album text, track_id int, title_track text, year_released int, month_released int, day_released int,' + 
    'artist text, duration int, genre text, favorites_artist int, listens_track int,' +
    'favorites_track int, listens_album int, favorites_album int,' +
    'PRIMARY KEY(genre, track_id));')

session.execute(
    'CREATE TABLE IF NOT EXISTS Q92 (' +
    'genre text, music_count counter, ' +
    'PRIMARY KEY(genre))')

session.execute(
    'CREATE TABLE IF NOT EXISTS Q93 (' +
    'genre text, music_count int, same_partition int,' +
    'PRIMARY KEY(same_partition, music_count, genre))' +
    'WITH CLUSTERING ORDER BY (music_count DESC);')

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
    insert_query = "INSERT INTO Q91(title_album, track_id, title_track, year_released, month_released, day_released," + \
        "artist, duration, genre, favorites_artist, listens_track," + \
        "favorites_track, listens_album, favorites_album) VALUES" + \
        "(\'{}\',{},\'{}\',{},{},{},\'{}\',{},\'{}\',{},{},{},{},{})".format(
        title_album, track_id, title_track, year_released, month_released, day_released, 
        artist, duration, genre, favorites_artist, listens_track,
        favorites_track, listens_album, favorites_album)
    if genre == '':
        continue
    session.execute(insert_query)

    # insert_statistics = "INSERT INTO Q92(genre, music_count) VALUES" + \
    #     "(\'{}\',{}) IF NOT EXISTS;".format(genre, 1)
    # session.execute(insert_statistics)
    update_statistic = "UPDATE Q92 " + \
        "SET music_count = music_count + 1 " + \
        "WHERE genre = \'{}\';".format(genre)
    session.execute(update_statistic)
# session.execute('COPY Q92(genre, music_count)' + \
#     'TO \'q92.csv\' WITH HEADER = TRUE ;')
# session.execute('COPY Q93(genre, music_count)' + \
#     'FROM \'q92.csv\' WITH HEADER = TRUE ;')
rows = session.execute('SELECT genre, music_count FROM Q92')
for row in rows:
    genre, count = row.genre, row.music_count
    insert_statistics = "INSERT INTO Q93(genre, music_count,same_partition) VALUES" + \
        "(\'{}\',{},1);".format(genre, count)
    session.execute(insert_statistics)
print("Data adding time: {} s".format(time.time() - start_time))

start_time = time.time()
rows = session.execute('SELECT genre, music_count FROM Q93')
print("Query time: {} s".format(time.time() - start_time))
print("Results:")
for row in rows:
    print("Genre: {}, Music Count: {}".format(row.genre, row.music_count))
