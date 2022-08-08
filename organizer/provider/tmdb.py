from functools import lru_cache

import tmdbsimple as tmdb


@lru_cache(maxsize=128)
def search_tv(query: str, api_key: str):
    """
    Search TV show by query.
    :param query: str
    :param api_key: TMDB API key.
    :return: dict
    """
    tmdb.API_KEY = api_key

    return tmdb.Search().tv(
        language="zh-CN",
        query=query,
        page=1,
        include_adults=True,
    )
