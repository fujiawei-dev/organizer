from functools import lru_cache
from time import sleep

import tmdbsimple as tmdb
from requests.exceptions import RequestException


@lru_cache(maxsize=128)
def search_tv(query: str, api_key: str, retry_count: int = 8) -> dict:
    """
    Search TV show by query.
    :param query: str
    :param api_key: TMDB API key.
    :param retry_count: int (default: 8)
    :return: dict
    """
    tmdb.API_KEY = api_key

    while retry_count > 0:
        try:
            return tmdb.Search().tv(
                language="zh-CN",
                query=query,
                page=1,
                include_adults=True,
            )
        except RequestException:
            retry_count -= 1
            if retry_count == 0:
                raise
            sleep(1)
            continue
