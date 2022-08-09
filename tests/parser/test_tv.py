import os

from organizer.parser.tv import TVParser, parse_tv_from_text
from tests.parser.test_tv_data import video_file_tv_pairs


def test_parse_tv_original_name():
    for text, expected in video_file_tv_pairs:
        assert TVParser.parse_original_name(text) == expected.original_name


def test_parse_tv_episode():
    for text, expected in video_file_tv_pairs:
        assert TVParser.parse_episode(text) == expected.episode


def test_parse_tv_season():
    for text, expected in video_file_tv_pairs:
        assert TVParser.parse_season(text) == expected.season


def test_parse_tv_from_text():
    for text, expected in video_file_tv_pairs:
        tv = parse_tv_from_text(text, os.getenv("TMDB__API_KEY"))
        assert tv.original_name == expected.original_name
        assert tv.chinese_name == expected.chinese_name
        assert tv.episode == expected.episode
        assert tv.season == expected.season
