import os.path
from pathlib import Path
from typing import NamedTuple, Union


class TestCarryData(NamedTuple):
    original_target_path: str
    content_size: int
    final_target_path: str
    handle_skipped_file: bool
    carry_tv: bool


test_carry_data = [
    TestCarryData("", 0, "", False, False),
    TestCarryData(
        original_target_path="[Nekomoe kissaten][Ai no Utagoe wo Kikasete][Movie][1080p][BDRip][JPSC].mp4",
        content_size=343,
        final_target_path="",
        handle_skipped_file=True,
        carry_tv=False,
    ),
    TestCarryData(
        original_target_path="[KyokuSai] Isekai Meikyuu de Harem wo [04][1080P][CHS].mp4",
        content_size=445,
        final_target_path="在异世界迷宫开后宫/Season 01/Episode S01E04.mp4",
        handle_skipped_file=True,
        carry_tv=True,
    ),
    TestCarryData(
        original_target_path="[KyokuSai] Isekai Meikyuu de Harem wo [05][1080P][CHS].mp4",
        content_size=45,
        final_target_path="在异世界迷宫开后宫/Season 01/Episode S01E05.mp4",
        handle_skipped_file=False,
        carry_tv=False,
    ),
    TestCarryData(
        original_target_path="[KyokuSai] Isekai Meikyuu de Harem wo [04][1080P][CHS].mp4.ass",
        content_size=12,
        final_target_path="在异世界迷宫开后宫/Season 01/Episode S01E04.mp4.ass",
        handle_skipped_file=True,
        carry_tv=True,
    ),
    TestCarryData(
        original_target_path="[LoliHouse] Kumichou Musume to Sewagakari - S1 04 [WebRip 1080p HEVC-10bit AAC SRTx2].mkv",
        content_size=385,
        final_target_path="组长女儿与照料专员/Season 01/Episode S01E04.mkv",
        handle_skipped_file=True,
        carry_tv=True,
    ),
    TestCarryData(
        original_target_path="[LoliHouse] Kumichou Musume to Sewagakari - S1 04 [WebRip 1080p HEVC-10bit AAC SRTx2].mkv",
        content_size=485,
        final_target_path="组长女儿与照料专员/Season 01/Episode S01E04.mkv",
        handle_skipped_file=True,
        carry_tv=True,
    ),
    TestCarryData(
        original_target_path="[NC-Raws] 王者天下 第四季 - 17 (Baha 1920x1080 AVC AAC MP4) [3B1AA7BB].mp4",
        content_size=302,
        final_target_path="王者天下/Season 04/Episode S04E17.mp4",
        handle_skipped_file=False,
        carry_tv=False,
    ),
    TestCarryData(
        original_target_path="[夜莺家族&YYQ字幕组]New Doraemon[17][2022.07.30][AVC][1080P][GB_JP].mp4",
        content_size=322,
        final_target_path="哆啦A梦/Season 01/Episode S01E17.mp4",
        handle_skipped_file=True,
        carry_tv=False,
    ),
]

skipped_keywords = {"王者天下", "哆啦A梦"}


def create_test_carry_data(temp_dir: Union[str, Path]):
    """Create test data."""
    for item in test_carry_data:
        if item.original_target_path:
            with open(os.path.join(temp_dir, item.original_target_path), "wb") as f:
                for _ in range(1024):
                    f.write(b"x" * (item.content_size * 1024))
