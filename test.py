import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

# create_table = "CREATE TABLE users (id int, username text, password text)"

# cursor.execute(create_table)


# user = (1, "admin", "admin")
#
# insert_query = "INSERT INTO users VALUES (?,?,?)"
# cursor.execute(insert_query, user)
# connection.commit()  # trzeba zatwierdzić zmiany commit
# connection.close()  # by ni eblokować innym połączenia z bazą


# users = [(2, "Andrzej", "password"), (3, "Maciej", "password")]
#
# insert_query = "INSERT INTO users VALUES (?,?,?)"
# cursor.executemany(insert_query, users)
# connection.commit()
# connection.close()


select_query = "SELECT * FROM users"
result = cursor.execute(select_query)
for user in result:
    print(user)

select_query = "SELECT * FROM movies"
result = cursor.execute(select_query)
for user in result:
    print(user)




# delete_query = "SELECT DISTINCT id, id FROM users"
# result = cursor.execute(delete_query)
# for user in result:
#     print(user)

# drop_query = "DROP TABLE users"
# cursor.execute(drop_query)


connection.close()