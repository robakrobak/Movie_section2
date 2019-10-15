from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

import sqlite3

movies = []


class MovieModel:
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre

    def __repr__(self):
        return f'Movie: {self.title}, Genre: {self.genre}'

    @classmethod
    def find_movie_by(cls, query, value):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        result = cursor.execute(query, value)
        row = result.fetchone()
        movie = None

        if row:
            movie = cls(row[0], row[1])  # *row  tworzymy obiekt

        connection.close()
        return movie

    @classmethod
    def find_by_movie_name(cls, name):
        query = "SELECT * FROM movies WHERE name=?"
        return cls.find_movie_by(query, (name,))

    @classmethod
    def find_by_movie_genre(cls, genre):
        query = "SELECT * FROM movies WHERE genre=?"
        return cls.find_movie_by(query, (genre,))

    def add_movie(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO movies VALUES (?, ?)"
        cursor.execute(query, (self.title, self.genre))
        connection.commit()  # trzeba zatwierdzić zmiany commit
        connection.close()  # by nie blokować innym połączenia z bazą

    def update_movie(self, genre):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE movies SET genre=? WHERE name=?"
        cursor.execute(query, (genre, self.title))
        connection.commit()
        connection.close()

    def to_dict(self):
        return {"title": self.title, "genre": self.genre}

    def delete_movie(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM movies WHERE name=?"
        cursor.execute(query, (self.title,))
        connection.commit()
        connection.close()

    @classmethod
    def get_movie_list(cls):
        movie_list = []
        query = "SELECT * FROM movies"
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        result = cursor.execute(query)

        for element in result:
            movie_list.append(cls(element[0], element[1]))
        connection.commit()
        connection.close()
        return movies


class Movie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "genre", type=str, required=True, help="This field cannot be left blank!"
    )

    # @jwt_required()
    def get(self, name):
        movie = MovieModel.find_by_movie_name(name)
        if movie:
            return {"name": movie.title, "genre": movie.genre}
        else:
            return {"message": "We coundn't find such a movie in our database."}, 404

    # def get(self, name):
    #     for movie in movies:
    #         if movie["name"] == name:
    #             return movie
    #     return {"message": "We coundn't find such a movie in our database."}, 404

    # powyzej dodaliśmy błąd 404 - bo oryginalnie flask wyrzuci 200

    def post(self, name):
        movie = MovieModel.find_by_movie_name(name)
        if movie:
            return {"message": "Movie already exists"}, 400
        data = Movie.parser.parse_args()
        movie = MovieModel(name, data["genre"])
        movie.add_movie()
        return movie.to_dict(), 201

    # def post(self, name):
    #     request_data = request.get_json()
    #     new_movie = {"name": name, "genre": request_data["genre"]}
    #     for movie in movies:
    #         if movie["name"] == name:
    #             return {"message": "Movie already exists"}, 409
    #     movies.append(new_movie)
    #     return new_movie, 201

    def delete(self, name):
        movie = MovieModel.find_by_movie_name(name)
        if movie:
            movie.delete_movie()
            return {"message": "movie deteted"}, 204
        return {"message": "movie with title does not exist"}, 404

    def put(self, name):
        data = Movie.parser.parse_args()
        movie = None
        status = 200

        movie = MovieModel.find_by_movie_name(name)

        if movie is None:
            movie = MovieModel(name, data["genre"])
            movie.add_movie()
        else:
            movie.update_movie(data["genre"])  # mozna wsadzić cokolwiek, niebezpieczenstwo
            status = 204

        movie = MovieModel.find_by_movie_name(name)  # zeby zupdateował

        return movie.to_dict(), status


class MovieList(Resource):
    @jwt_required
    def get(self):
        movie_list = [movie.to_dict() for movie in MovieModel.get_movie_list()]
        return {"movies": "movie_list"}

# class MovieList(Resource):
#     def get(self):
#         return {"movies": movies}

# test = MovieModel.find_by_movie_name("movie1")
# print(test)
#
# test1 = MovieModel.find_by_movie_genre("Comedy")
# print(test1)

# test2 = MovieModel.find_by_movie_id("1")
# print(test2)
