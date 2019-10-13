import sqlite3
from flask_restful import Resource, reqparse
from flask import request


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'User id: {self.id}, user name: {self.username}, password: encrypted.'

    # @classmethod                                # metoda klasowa
    # def find_by_username(cls, username):        # metoda klasowa
    #     connection = sqlite3.connect("data.db")
    #     cursor = connection.cursor()
    #     query = "SELECT * FROM users WHERE username=?"
    #
    #     # (username,) musi być tupla! - krotka, cos co ma wiecej niz 1 element
    #     result = cursor.execute(query, (username,))
    #
    #     # wyciąga dokładnie pierwszy
    #     row = result.fetchone()
    #
    #     user = None
    #
    #     if row:
    #         user = cls(row[0], row[1], row[2])  # *row
    #
    #     connection.commit()
    #     connection.close()
    #     return user
    #
    # @classmethod
    # def find_user_by_id(cls, user_id):
    #     connection = sqlite3.connect("data.db")
    #     cursor = connection.cursor()
    #     query = "SELECT * FROM users WHERE id=?"
    #
    #     result = cursor.execute(query, (user_id,))
    #     row = result.fetchone()
    #
    #     user = None
    #
    #     if row:
    #         user = cls(row[0], row[1], row[2])  # *row
    #
    #     connection.commit()
    #     connection.close()
    #     return user

    # czystsza wersja do wersji gdzie trzeba szukać po większej ilości zapytań...

    @classmethod
    def find_by_username(cls, username):
        query = "SELECT * FROM users WHERE username=?"
        return cls.find_by(query, (username,))

    @classmethod
    def find_by_id(cls, _id):
        query = "SELECT * FROM users WHERE id=?"
        return cls.find_by(query, (_id,))

    @classmethod
    def find_by(cls, query, value):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        result = cursor.execute(query, value)
        row = result.fetchone()
        user = None

        if row:
            user = cls(row[0], row[1], row[2])  # *row

        connection.commit()
        connection.close()
        return user


class UserRegister(Resource):
    #formatuje dane, które wklepuje użytkownik
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )

    def post(self):
        data_user = UserRegister.parser.parse_args()
        #w ten sposób:
        if User.find_by_username(data_user["username"]):
            return {"message": "user already exists"}, 400
        #lub w ten sposób:
        # username = data_user["username"]
        #   if User.find_by_username(username):


        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        insert_query = "INSERT INTO users VALUES (NULL,?,?)"
        # to
        # username = data_user["username"]
        # user_password = data_user["password"]
        # cursor.execute(insert_query, (username, user_password))
        #lub to
        cursor.execute(insert_query, data_user["username"], data_user["password"])

        connection.commit()  # trzeba zatwierdzić zmiany commit
        connection.close()  # by nie blokować innym połączenia z bazą

        return {"message": "user created"}


# test1 = User.find_by_id(1)
# print(test1)
#
# test2 = User.find_by_id(2)
# print(test2)
#
# test3 = User.find_by_id(3)
# print(test3)
#
# test_by_username = User.find_by_username("admin")
# print(test_by_username)
