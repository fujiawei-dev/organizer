import re

from pydantic import BaseModel

from organizer.logger import logging
from organizer.provider.tmdb import search_tv

log = logging.getLogger(__name__)


class TV(BaseModel):
    original_name: str = ""
    chinese_name: str = ""
    episode: int = 1
    season: int = 1


class TVParser(object):
    @staticmethod
    def parse_original_name(text: str) -> str:
        val = ""

        if match := re.search(r"]\s*([^]]{3,}?)\s*[\[(]", text):
            val = match.group(1)

        elif len(matches := re.findall(r"\[(.*?)]", text)) > 1:
            val = matches[1]

        if val:
            if (dash := val.rfind(" - ")) > 0:
                val = val[:dash]

            val = re.sub(r"[_\-·！？。]", " ", val)
            val = re.sub(r"[!?，]", "", val)

            val_zh = re.sub("[\u4e00-\u9fa5]", "", val).strip()

            if val_zh != val and len(val_zh) < 12:
                log.debug(f"{val!r} vs {val_zh!r}")
                if (end := val.find(" ")) > 0:
                    val = val[:end]
            else:
                val = val_zh
                val = re.sub(r"s\d+", " ", val, flags=re.IGNORECASE)
                val = re.sub(r" \d+\w+ ?season", " ", val, flags=re.IGNORECASE)

            val = re.sub(r"\d", " ", val)

        if val:
            val = re.sub(r"\s{2,}", " ", val).strip()

        return val

    @staticmethod
    def parse_episode(text: str) -> int:
        text = re.sub(r"[_-]", " ", text)

        if val := (re.search(r"\[(\d{1,2})]", text) or re.search(r" (\d{2}) ", text)):
            val = val.group(1)

        return int(val) if val else 1

    @staticmethod
    def parse_season(text: str) -> int:
        text = re.sub(r"[_-]", " ", text)

        if val := re.search(r"S(\d)", text):
            val = val.group(1)
        elif val := re.search(r"(\d+)\w+ ?season", text, flags=re.IGNORECASE):
            val = val.group(1)
        elif val := re.search(r"([一二三四五六七八九十])季", text):
            val = "一二三四五六七八九十".index(val.group(1)) + 1

        return int(val) if val else 1


def parse_tv_from_text(text: str, api_key: str) -> TV:
    tv = TV(
        original_name=TVParser.parse_original_name(text),
        episode=TVParser.parse_episode(text),
        season=TVParser.parse_season(text),
    )

    if tv.original_name:
        response: dict = search_tv(tv.original_name, api_key=api_key)

        if results := response.get("results"):
            tv.chinese_name = results[0].get("name", "")

        if not tv.chinese_name:
            log.debug(response)
            log.error(f"No results for {tv.original_name!r}")

    return tv
