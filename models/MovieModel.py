import json

from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    imdb_id = db.Column(db.String, nullable=False)

    def json(self):
        return {
            'name': self.name,
            'year': self.year,
            'director': self.director,
            'imdb_id': self.imdb_id
        }

    @staticmethod
    def add_movie(_name, _year, _director, _imdb_id):
        new_movie = Movie(name=_name, year=_year, director=_director, imdb_id=_imdb_id)
        db.session.add(new_movie)
        db.session.commit()

    @staticmethod
    def get_all_movies():
        return [movie.json() for movie in Movie.query.all()]

    @staticmethod
    def get_movie(_imdb_id):
        return Movie.query.filter_by(imdb_id=_imdb_id).first().json()

    @staticmethod
    def delete_movie(_imdb_id):
        status = Movie.query.filter_by(imdb_id=_imdb_id).delete()
        db.session.commit()
        return bool(status)

    @staticmethod
    def update_movie_name(_imdb_id, _name):
        movie_to_update = Movie.query.filter_by(imdb_id=_imdb_id).first()
        movie_to_update.name = _name
        db.session.commit()

    @staticmethod
    def update_movie_year(_imdb_id, _year):
        movie_to_update = Movie.query.filter_by(imdb_id=_imdb_id).first()
        movie_to_update.year = _year
        db.session.commit()

    @staticmethod
    def update_movie_director(_imdb_id, _director):
        movie_to_update = Movie.query.filter_by(imdb_id=_imdb_id).first()
        movie_to_update.director = _director
        db.session.commit()

    @staticmethod
    def replace_movie(_imdb_id, _name, _year, _director):
        movie_to_replace = Movie.query.filter_by(imdb_id=_imdb_id).first()
        movie_to_replace.name = _name
        movie_to_replace.year = _year
        movie_to_replace.director = _director
        db.session.commit()

    def __repr__(self):
        movie_object = {
            'name': self.name,
            'year': self.year,
            'director': self.director,
            'imdb_id': self.imdb_id
        }
        return json.dumps(movie_object)
