import contextlib
import os.path
import shutil
from pathlib import Path
from typing import Union

from organizer.config.ignore import Ignore, should_be_skipped
from organizer.logger import logging
from organizer.parser.tv import parse_tv_from_text

log = logging.getLogger(__name__)


def dry_run_or_unlink(item: Union[Path, str], dry_run: bool):
    if not dry_run:
        Path(item).unlink(missing_ok=True)


def generate_tv_video_path(
    item: Union[str, Path],
    dst: Union[str, Path],
    api_key: str,
    ignore: Ignore,
    dry_run: bool = False,
) -> Union[str, Path, None]:
    item = Path(item)

    tv = parse_tv_from_text(item.stem, api_key)

    if not tv.original_name:
        log.error('No original name found for "%s"' % item.stem)
        return

    if not tv.chinese_name:
        log.error('No chinese name found for "%s"' % item.stem)
        dry_run_or_unlink(item, dry_run)
        return

    if should_be_skipped(tv.chinese_name.upper(), ignore.skipped_keywords):
        log.info(f"{tv.chinese_name} should be skipped")
        dry_run_or_unlink(item, dry_run)
        return

    season = os.path.join(dst, tv.chinese_name, f"Season {tv.season:02d}")

    if not os.path.exists(season):
        if not dry_run:
            try:
                os.makedirs(season)
            except NotADirectoryError:
                log.debug(item)
                log.error(f"{season} is not a directory.")
                return

    episode = f"Episode S{tv.season:02d}E{tv.episode:02d}"

    if len(item.suffixes) > 1:
        suffix = "".join(
            s
            for s in item.suffixes
            if s in ignore.video_file_suffixes or s in ignore.subtitle_file_suffixes
        )
    else:
        suffix = item.suffix

    name = os.path.join(season, f"{episode}{suffix}")

    for video_suffix in ignore.video_file_suffixes:
        file = os.path.join(season, f"{episode}{video_suffix}")

        if os.path.exists(file):
            if os.path.getsize(item) > os.path.getsize(file) + 1024 * 1024 * 100:
                log.debug("%s is larger than %s" % (item, file))
                dry_run_or_unlink(file, dry_run)
            else:
                log.debug("%s is smaller than %s, skipped" % (item, file))
                dry_run_or_unlink(item, dry_run)
                return

    return name


def handle_skipped_files(item: Path, ignore: Ignore, dry_run: bool) -> bool:
    """If the file is skipped, remove it."""
    if not item.is_file():
        log.info(f"{item} is not a file")
        return False

    if item.suffix not in ignore.not_skipped_file_suffixes:
        item.unlink(missing_ok=True)
        return False

    if (
        item.suffix not in ignore.subtitle_file_suffixes
        and os.path.getsize(item) < 1024 * 1024 * ignore.minimum_file_size
    ):
        log.info(f"{item} is too small, skipped.")
        dry_run_or_unlink(item, dry_run)
        return False

    if should_be_skipped(item.stem.upper(), ignore.skipped_keywords):
        log.info(f"{item} is skipped.")
        dry_run_or_unlink(item, dry_run)
        return False

    return True


def carry_tv(
    src: Union[str, Path],
    dst: Union[str, Path],
    ignore: Ignore,
    api_key: str,
    dry_run=False,
):
    for item in Path(src).iterdir():
        if item.is_dir():
            if item.name in ignore.ignore_dirs:
                log.info(f"{item} is ignored")
                continue
            carry_tv(item, dst, ignore, api_key, dry_run)
            with contextlib.suppress(PermissionError, OSError):
                item.rmdir()
        elif item.is_file() and handle_skipped_files(item, ignore, dry_run):
            if path := generate_tv_video_path(item, dst, api_key, ignore, dry_run):
                log.info(f"{item} -> {path}")
                if not dry_run:
                    shutil.move(item, path)
