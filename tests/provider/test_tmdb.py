import os

from organizer.provider.tmdb import search_tv


def test_search_tv():
    left = search_tv("Isekai Meikyuu de Harem wo", os.getenv("TMDB__API_KEY"))
    right = search_tv("在异世界迷宫开后宫", os.getenv("TMDB__API_KEY"))
    assert left == right
