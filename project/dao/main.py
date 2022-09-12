from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc

from project.dao.base import BaseDAO, T
from project.models import *


class GenreDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorDAO(BaseDAO[Director]):
    __model__ = Director


class MovieDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all(self, page: Optional[int] = None, status=None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)

        if status and status == 'new':
            stmt = stmt.order_by(desc(Movie.year))

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UserDAO(BaseDAO[User]):
    __model__ = User

    def create(self, data):
        try:
            user = User(**data)
            self._db_session.add(user)
            self._db_session.commit()
            return user
        except IntegrityError:
            return None

    def get_by_user_email(self, email):
        user = self._db_session.query(User).filter(User.email == email).one_or_none()
        return user

    def patch(self, user):
        self._db_session.add(user)
        self._db_session.commit()

    def update_password(self, user):
        self._db_session.add(user)
        self._db_session.commit()



