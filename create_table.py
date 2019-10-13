import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS movies (name text, genre text)"
cursor.execute(query)

# movies = [("movie1", "Horror"), ("movie2", "Horror"), ("movie3", "Comedy")]
# insert_query = "INSERT INTO movies VALUES (?, ?)"
# cursor.executemany(insert_query, movies)



connection.commit()
connection.close()

