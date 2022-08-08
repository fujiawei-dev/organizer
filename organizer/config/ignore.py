from pydantic import BaseModel

VIDEO_FILE_SUFFIXES = {".mkv", ".mp4", ".flv", ".avi", ".mov"}

SUBTITLE_FILE_SUFFIXES = {".srt", ".sub", ".ass"}

IGNORE_DIRS = {"_gsdata_"}

MINIMUM_FILE_SIZE = 200  # MB


class Ignore(BaseModel):
    minimum_file_size: int = MINIMUM_FILE_SIZE

    video_file_suffixes: set[str] = VIDEO_FILE_SUFFIXES
    subtitle_file_suffixes: set[str] = SUBTITLE_FILE_SUFFIXES

    ignore_dirs: set[str] = IGNORE_DIRS
    skipped_keywords: set[str] = {}
    delete_skipped_videos: bool = True

    @property
    def not_skipped_file_suffixes(self) -> set[str]:
        return self.video_file_suffixes | self.subtitle_file_suffixes


def should_be_skipped(text: str, skipped_keywords: set[str]) -> bool:
    for keyword in skipped_keywords:
        if keyword in text:
            return True
    return False
