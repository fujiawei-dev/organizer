import contextlib
import os
import tempfile
from pathlib import Path

from organizer.config.ignore import Ignore
from organizer.runner.carry import (
    carry_tv,
    dry_run_or_unlink,
    generate_tv_video_path,
    handle_skipped_files,
)
from tests.runner.test_carry_data import (
    create_test_carry_data,
    skipped_keywords,
    test_carry_data,
)


def test_dry_run_or_unlink():
    temp_dir = Path(tempfile.mkdtemp())
    item = temp_dir / "item"

    item.touch(exist_ok=True)
    dry_run_or_unlink(item, dry_run=True)
    assert item.exists()

    item.touch(exist_ok=True)
    dry_run_or_unlink(item, dry_run=False)
    assert not item.exists()


def test_generate_tv_video_path():
    api_key = os.getenv("TMDB__API_KEY")

    temp_src = Path(tempfile.mkdtemp())
    create_test_carry_data(temp_src)

    temp_dst_1 = Path(tempfile.mkdtemp())
    temp_dst_2 = Path(tempfile.mkdtemp())

    for item in test_carry_data:
        expected_path = os.path.join(temp_dst_1, item.final_target_path)

        if file_path := generate_tv_video_path(
            temp_src / item.original_target_path,
            dst=temp_dst_1,
            api_key=api_key,
            ignore=Ignore(),
            dry_run=False,
        ):
            assert os.path.normpath(file_path) == os.path.normpath(expected_path)

        expected_path = os.path.join(temp_dst_2, item.final_target_path)
        with contextlib.suppress(ValueError):
            if file_path := generate_tv_video_path(
                item.original_target_path,
                dst=temp_dst_2,
                api_key=api_key,
                ignore=Ignore(),
                dry_run=True,
            ):
                assert os.path.normpath(file_path) == os.path.normpath(expected_path)


def test_handle_skipped_files():
    temp_dir = Path(tempfile.mkdtemp())
    create_test_carry_data(temp_dir)

    for item in test_carry_data:
        assert (
            handle_skipped_files(
                temp_dir / item.original_target_path,
                Ignore(
                    skipped_keywords=skipped_keywords,
                ),
                dry_run=False,
            )
            == item.handle_skipped_file
        )


def test_carry_tv():
    api_key = os.getenv("TMDB__API_KEY")

    temp_dir = Path(tempfile.mkdtemp())

    src = temp_dir / "src"
    src_sub = src / "sub"
    src_ignore = src / "_gsdata_"
    dst = temp_dir / "dst"

    src.mkdir()
    src_sub.mkdir()
    src_ignore.mkdir()
    dst.mkdir()

    create_test_carry_data(src)
    create_test_carry_data(src_sub)
    create_test_carry_data(src_ignore)

    carry_tv(
        src,
        dst,
        Ignore(
            ignore_dirs={"_gsdata_"},
            skipped_keywords=skipped_keywords,
        ),
        api_key,
        dry_run=False,
    )

    for item in test_carry_data:
        assert not item.carry_tv or os.path.exists(dst / item.final_target_path)

        if item.original_target_path:
            assert os.path.exists(src_ignore / item.original_target_path)
