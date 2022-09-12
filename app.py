from flask import request
from flask_restx import Api, Resource
from config import app, db
from models import Movie, Director, Genre
from schemas import MovieSchema, DirectorSchema, GenreSchema

# Создание неймспейсов
api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

# Создание схем
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    """
    Представление для всех фильмов
    """
    def get(self):
        """
        Метод для получения всех фильмов
        """
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        query = Movie.query

        if director_id:
            query = query.filter(Movie.director_id == director_id)
        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)
        result = movies_schema.dump(query.all())
        return result, 200

    def post(self):
        """
        Метод для добавления фильма в базу данных
        """
        req_json = request.json
        try:
            new_movie = Movie(**req_json)
            with db.session.begin():
                db.session.add(new_movie)
            return "Добавление успешно", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Ошибка", 500


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    """
    Представление для одного фильма
    """
    def get(self, mid):
        """
        Метод для получения одного фильма
        """
        movie = Movie.query.get(mid)
        if not movie:
            return "Ошибка", 404
        return movie_schema.dump(movie), 200

    def put(self, mid):
        """
        Метод для обновления данных одного фильма
        """
        movie = Movie.query.get(mid)
        if not movie:
            return "Ошибка", 404
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "Обновление успешно", 204

    def delete(self, mid):
        """
        Метод для удаления одного фильма
        """
        movie = Movie.query.get(mid)
        if not movie:
            return "Ошибка", 404
        db.session.delete(movie)
        db.session.commit()
        return "Удаление успешно", 204


@director_ns.route('/')
class DirectorsView(Resource):
    """
    Представление для всех режиссеров
    """
    def get(self):
        """
        Метод для получения всех режиссеров
        """
        result = directors_schema.dump(Director.query.all())
        return result, 200

    def post(self):
        """
        Метод для добавления режиссера в базу данных
        """
        req_json = request.json
        try:
            new_director = Director(**req_json)
            with db.session.begin():
                db.session.add(new_director)
            return "Добавление успешно", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Ошибка", 500


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    """
    Представление для одного режиссера
    """
    def get(self, did):
        """
        Метод для получения одного режиссера
        """
        director = Director.query.get(did)
        if not director:
            return "Ошибка", 404
        return director_schema.dump(director), 200

    def put(self, did):
        """
        Метод для обновления данных одного режиссера
        """
        director = Director.query.get(did)
        if not director:
            return "", 404
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "Обновление успешно", 204

    def delete(self, did):
        """
        Метод для удаления одного режиссера
        """
        director = Director.query.get(did)
        if not director:
            return "Ошибка", 404
        db.session.delete(director)
        db.session.commit()
        return "Удаление успешно", 204


@genre_ns.route('/')
class GenresView(Resource):
    """
    Представление для всех жанров
    """
    def get(self):
        """
        Метод для получения всех жанров
        """
        result = genres_schema.dump(Genre.query.all())
        return result, 200

    def post(self):
        """
        Метод для добавления жанра в базу данных
        """
        req_json = request.json
        try:
            new_genre = Genre(**req_json)
            with db.session.begin():
                db.session.add(new_genre)
            return "Добавление успешно", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Ошибка", 500


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    """
    Представление для одного жанра
    """
    def get(self, gid):
        """
        Метод для получения одного жанра
        """
        genre = Genre.query.get(gid)
        if not genre:
            return "Ошибка", 404
        return genre_schema.dump(genre), 200

    def put(self, gid):
        """
        Метод для обновления данных одного жанра
        """
        genre = Genre.query.get(gid)
        if not genre:
            return "Ошибка", 404
        req_json = request.json
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "Обновление успешно", 204

    def delete(self, gid):
        """
        Метод для удаления одного жанра
        """
        genre = Genre.query.get(gid)
        if not genre:
            return "Ошибка", 404
        db.session.delete(genre)
        db.session.commit()
        return "Удаление успешно", 204


if __name__ == '__main__':
    app.run(debug=True)
