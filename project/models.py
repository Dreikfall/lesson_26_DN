from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genre'
    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'director'
    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movie'
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    trailer = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    director_id = Column(Integer, ForeignKey('director.id'))
    genre = relationship('Genre')
    director = relationship('Director')


class User(models.Base):
    __tablename__ = 'user'
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favourite_genre = Column(Integer, ForeignKey('genre.id'))
    genre = relationship('Genre')










