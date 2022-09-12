from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссеры', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тарантино'),
})

movie: Model = api.model('Фильмы', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Вий'),
    'description': fields.String(required=True, max_length=250, example='Описание'),
    'trailer': fields.String(required=True, max_length=100, example='youtube'),
    'year': fields.Integer(required=True, example=1999),
    'rating': fields.Float(required=True, example=5.6),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director)
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='qwerty@mail.ru'),
    'password': fields.String(required=True, max_length=100, example='76g7iTG&I'),
    'name': fields.String(required=True, max_length=100, example='Nik'),
    'surname': fields.String(required=True, max_length=100, example='Drinkens'),
    'genre': fields.Nested(genre)
})



