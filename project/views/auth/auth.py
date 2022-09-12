from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('auth')


@api.route('/register')
class AuthView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        data = request.json

        email = data.get('email')
        password = data.get('password')
        if None in (email, password):
            return "Parameters passed incorrectly", 400
        user = user_service.create(data)
        if not user:
            return "User with this email is already registered", 400
        return "", 201, {"location": f'/auth/{user.id}'}


@api.route('/login')
class AuthView(Resource):
    def post(self):
        data = request.json

        email = data.get('email')
        password = data.get('password')
        if None in (email, password):
            return "", 400
        try:
            tokens = user_service.generate_tokens(email, password)
            return tokens, 201
        except Exception:
            return "Invalid data entered"

    def put(self):
        tokens = request.json
        if None in (tokens["access_token"], tokens["refresh_token"]):
            return "", 400
        tokens = user_service.approve_refresh_token(tokens)
        return tokens, 201
