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
            movie = cls(row[0], row[1])  # *row

        connection.close()
        return movie

    @classmethod
    def find_by_movie_name(cls, name):
        query = "SELECT * FROM movies WHERE name=?"
        return cls.find_movie_by(query, (name,))

    @classmethod
    def find_by_movie_id(cls, _id):
        query = "SELECT * FROM movies WHERE id=?"
        return cls.find_movie_by(query, (_id,))

    @classmethod
    def find_by_movie_genre(cls, genre):
        query = "SELECT * FROM movies WHERE genre=?"
        return cls.find_movie_by(query, (genre,))




class Movie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "genre", type=str, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        for movie in movies:
            if movie["name"] == name:
                return movie
        return {"message": "We coundn't find such a movie in our database."}, 404

    # powyzej dodaliśmy błąd 404 - bo oryginalnie flask wyrzuci 200

    def post(self, name):
        request_data = request.get_json()
        new_movie = {"name": name, "genre": request_data["genre"]}
        for movie in movies:
            if movie["name"] == name:
                return {"message": "Movie already exists"}, 409
        movies.append(new_movie)
        return new_movie, 201

    def delete(self, name):
        global movies  # global jest potrzebny tutaj, bo funkcja nie zna tej zmiennej movies....
        temp_list = []
        for movie in movies:
            if movie["name"] != name:
                temp_list.append(movie)
        movies = temp_list
        return {"message": "movie deteted"}

    def put(self, name):
        # data = request.get_json()
        data = Movie.parser.parse_args()
        movie = None
        status = 200

        for _movie in movies:
            if _movie["name"] == name:
                movie = _movie

        if movie is None:
            movie = {"name": name, "genre": data["genre"]}
            movies.append(movie)
        else:
            movie.update(data)  # mozna wsadzić cokolwiek, niebezpieczenstwo
            status = 204

        return movie, status


class MovieList(Resource):
    def get(self):
        return {"movies": movies}


test = MovieModel.find_by_movie_name("movie1")
print(test)

test1 = MovieModel.find_by_movie_genre("Comedy")
print(test1)

# test2 = MovieModel.find_by_movie_id("1")
# print(test2)

