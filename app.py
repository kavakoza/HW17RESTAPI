# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movies_schema = MovieSchema()
directors_schema = DirectorSchema()
genres_schema = GenreSchema()


# регистрирация класса Movie по определенному пути
@movie_ns.route('/')
class MoviesView(Resource):

    def get(self):

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        x = Movie.query

        if director_id:
            x = x.filter(Movie.director_id == director_id)
        if genre_id:
            x = x.filter(Movie.genre_id == genre_id)
        all_movies = x.all()

        return movies_schema.dump(all_movies, many=True), 200


    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return '', 201


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):

    def get(self, mid: int):
        try:
            movie = Movie.query.get(mid)
            return movies_schema.dump(movie), 200
        except Exception as e:
            return '', 404


    def put(self, mid: int):
        movie = Movie.query.get(mid)
        req_json = request.json

        movie.name = req_json.get('name')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')

        db.session.add(movie)
        db.session.commit()
        return '', 204


    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return '', 204


# регистрирация класса Director по определенному пути
@director_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        all_directors = Director.query.all()
        return directors_schema.dump(all_directors, many=True), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return '', 201

    def put(self, did: int):
        director = Director.query.get(did)
        req_json = request.json

        director.name = req_json.get('name')

        db.session.add(director)
        db.session.commit()
        return '', 204

    def delete(self, did: int):
        director = Director.query.get(did)
        db.session.delete(director)
        db.session.commit()
        return '', 204

# регистрирация класса Genre по определенному пути
@genre_ns.route('/')
class GenresView(Resource):

    def get(self):
        all_genres = Genre.query.all()
        return genres_schema.dump(all_genres, many=True), 200


    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return '', 201


    def put(self, gid: int):
        genre = Genre.query.get(gid)
        req_json = request.json

        genre.name = req_json.get('name')

        db.session.add(genre)
        db.session.commit()
        return '', 204


    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        db.session.delete(genre)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
