from flask import request
from flask_restx import Namespace, Resource
from project.setup.api.models import user
from project.container import user_service
from project.tools.security import auth_required

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @auth_required
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        data_head = request.headers["Authorization"]
        token = data_head.split('Bearer ')[-1]
        user_ = user_service.get_user_by_tokens(token)
        if user_ is None:
            return 'token(s) missing or decoding problem'
        return user_, 200

    @auth_required
    def patch(self):
        data_head = request.headers["Authorization"]
        token = data_head.split('Bearer ')[-1]
        data_json = request.json
        user_service.update(token, data_json)
        return "", 204


@api.route('/password')
class UserView(Resource):
    @auth_required
    def put(self):
        data_head = request.headers["Authorization"]
        token = data_head.split('Bearer ')[-1]
        data_json = request.json
        if None in (data_json['old_password'], data_json['new_password']):
            return "Password(s) not sent"
        if user_service.update_password(token, data_json['old_password'], data_json["new_password"]) == "Error":
            return "The old password was entered incorrectly", 400
        return "", 204
