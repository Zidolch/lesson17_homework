import models
from marshmallow import Schema, fields


class DirectorSchema(Schema):
    """
    Схема для сериализации данных режиссера
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    """
    Схема для сериализации данных жанра
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()


class MovieSchema(Schema):
    """
    Схема для сериализации данных фильма
    """
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    director = fields.Pluck(DirectorSchema, 'name')
    genre = fields.Pluck(GenreSchema, 'name')
