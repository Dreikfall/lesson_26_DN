from typing import Optional

from project.dao import MovieDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MovieService:
    def __init__(self, dao: MovieDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Movie with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None, status=None) -> list[Movie]:
        return self.dao.get_all(page=page, status=status)
