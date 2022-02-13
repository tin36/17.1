# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


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
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.String()

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.String()

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = DirectorSchema()
genres_schema = DirectorSchema(many=True)


api = Api(app)
movie_ns = api.namespace('movies')
genre_ns = api.namespace('genres')
direcor_ns = api.namespace('directors')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id and genre_id:
            movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id)
        elif director_id:
            movies = Movie.query.filter_by(director_id=director_id)
        elif genre_id:
            movies = Movie.query.filter_by(genre_id=genre_id)
        else:
            movies = Movie.query.all()
        return movies_schema.dump(movies), 200,  {'Content-Type': 'application/json; charset=utf-8'}

@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie = Movie.query.get(id)
        return movie_schema.dump(movie), 200,  {'Content-Type': 'application/json; charset=utf-8'}

@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genre = Genre.query.all()
        return genres_schema.dump(genre), 200,  {'Content-Type': 'application/json; charset=utf-8'}
    def post(self):
        req_json = request.json
        genre_add = Genre(**req_json)
        with db.session.begin():
            db.session.add(genre_add)
        return '', 201





@genre_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        genre = Genre.query.get(id)
        return genre_schema.dump(genre), 200,  {'Content-Type': 'application/json; charset=utf-8'}

    def put(self, id):
        genre = Genre.query.get(id)
        if genre:
            req_json = request.json
            genre.name = req_json.get('name')
            db.session.add(genre)
            db.session.commit()
            return '', 200
        else:
            return '', 404

    def delete(self, id):
        genre = Genre.query.get(id)
        if genre:
            db.session.delete(genre)
            db.session.commit()
            return '', 204
        else:
            return '', 404

    def patch(self, id):
        genre = Genre.query.get(id)
        req_json = request.json
        if 'name' in req_json:
            genre.name = req_json.get('name')
            db.session.add(genre)
            db.session.commit()
            return '', 204
        else:
            return '', 404

@direcor_ns.route('/')
class DirectorView(Resource):
    def get(self):
        director = Director.query.all()
        return directors_schema.dump(director), 200,  {'Content-Type': 'application/json; charset=utf-8'}
    def post(self):
        req_json = request.json
        director_add = Director(**req_json)
        with db.session.begin():
            db.session.add(director_add)
        return '', 201

@direcor_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id):
        director = Director.query.get(id)
        return director_schema.dump(director), 200,  {'Content-Type': 'application/json; charset=utf-8'}

    def put(self, id):
        director = Director.query.get(id)
        if director:
            req_json = request.json
            director.name = req_json.get('name')
            db.session.add(director)
            db.session.commit()
            return '', 200
        else:
            return '', 404

    def delete(self, id):
        director = Director.query.get(id)
        if director:
            db.session.delete(director)
            db.session.commit()
            return '', 204
        else:
            return '', 404

    def patch(self, id):
        director = Director.query.get(id)
        req_json = request.json
        if 'name' in req_json:
            director.name = req_json.get('name')
            db.session.add(director)
            db.session.commit()
            return '', 204
        # else:
        #     return '', 404



if __name__ == '__main__':
    app.run(debug=True)
