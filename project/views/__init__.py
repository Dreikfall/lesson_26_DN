from .auth import auth_ns, user_ns
from .main import genres_ns, directors_ns, movies_ns

__all__ = [
    'auth_ns',
    'genres_ns',
    'directors_ns',
    'user_ns',
    'movies_ns'
]
