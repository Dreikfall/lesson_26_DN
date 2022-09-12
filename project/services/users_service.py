import base64
import calendar
import datetime
import hashlib
import hmac
from typing import Optional

import jwt
from flask_restx import abort
from jwt import DecodeError, InvalidSignatureError

from project.config import BaseConfig as BC
from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.models import User


class UserService:
    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create(self, data):
        data['password'] = self.generate_password(data['password'])
        return self.dao.create(data)

    def update(self, token, data):
        user = self.get_user_by_tokens(token)
        if 'name' in data:
            user.name = data.get('name')
        if 'surname' in data:
            user.surname = data.get('surname')
        if 'favorite_genre' in data:
            user.favorite_genre = data.get('favorite_genre')
        return self.dao.patch(user)

    def get_by_user_email(self, email):
        return self.dao.get_by_user_email(email)

    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            BC.PWD_SALT,
            BC.PWD_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def generate_tokens(self, email, password, is_tokens=False):
        """Функция генерации токенов"""
        user = self.dao.get_by_user_email(email)
        if user is None:
            raise abort(404)
        if not is_tokens:
            if not self.compare_passwords(user.password, password):
                abort(400)
        data = {
            'email': user.email
        }
        # 30 minutes for acces token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, BC.SECRET_KEY, algorithm=BC.JWT_ALGORITHM)

        # 100 days for refresh_token
        days100 = datetime.datetime.utcnow() + datetime.timedelta(days=100)
        data['exp'] = calendar.timegm(days100.timetuple())
        refresh_token = jwt.encode(data, BC.SECRET_KEY, algorithm=BC.JWT_ALGORITHM)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode(),
            BC.PWD_SALT,
            BC.PWD_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)

    def approve_refresh_token(self, tokens):
        """Генерация новых токенов из валидных токенов"""
        try:
            data = jwt.decode(jwt=tokens["access_token"], key=BC.SECRET_KEY, algorithms=[BC.JWT_ALGORITHM])
            email = data.get('email')
            return self.generate_tokens(email, None, is_tokens=True)
        except DecodeError:
            try:
                data = jwt.decode(jwt=tokens["refresh_token"], key=BC.SECRET_KEY, algorithms=[BC.JWT_ALGORITHM])
                email = data.get('email')
                return self.generate_tokens(email, None, is_tokens=True)
            except Exception:
                return "tokens have not been validated"

    def get_user_by_tokens(self, tokens):
        if isinstance(tokens, str):
            try:
                data = jwt.decode(jwt=tokens, key=BC.SECRET_KEY, algorithms=[BC.JWT_ALGORITHM])
                email = data.get('email')
                return self.dao.get_by_user_email(email)
            except InvalidSignatureError:
                return None
        try:
            data = jwt.decode(jwt=tokens["access_token"], key=BC.SECRET_KEY, algorithms=[BC.JWT_ALGORITHM])
            email = data.get('email')
            return self.dao.get_by_user_email(email)
        except InvalidSignatureError:
            try:
                data = jwt.decode(jwt=tokens["refresh_token"], key=BC.SECRET_KEY, algorithms=[BC.JWT_ALGORITHM])
                email = data.get('email')
                return self.dao.get_by_user_email(email)
            except InvalidSignatureError:
                return None

    def update_password(self, token, old_password, new_password):
        user = self.get_user_by_tokens(token)
        real_str_user_password = user.password
        if not self.compare_passwords(real_str_user_password, old_password):
            return "Error"
        user.password = self.generate_password(new_password)
        return self.dao.update_password(user)
