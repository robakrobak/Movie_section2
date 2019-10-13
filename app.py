from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister
from movie import Movie, MovieList

# Resource - reprezentacja jakiegoś konkretnego bytu
# zazwyczaj ma odzwierceidelenie w tabeli

app = Flask(__name__)
api = Api(app)


app.secret_key = "my-secret-key"
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(Movie, '/movie/<string:name>'),
api.add_resource(MovieList, '/movies')
api.add_resource(UserRegister, '/register')

app.run(debug=True)
