from pydantic import HttpUrl, ValidationError

from repository.implementations.user_cache_repository import ValueType


def link_filter(text):
    HttpUrl(text)
    return text