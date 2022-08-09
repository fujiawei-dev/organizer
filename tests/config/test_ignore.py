from organizer.config.ignore import Ignore, should_be_skipped


def test_ignore():
    ignore = Ignore(delete_skipped_videos=False)
    assert not ignore.delete_skipped_videos


def test_should_be_skipped():
    ignore = Ignore(skipped_keywords={"720"})

    assert should_be_skipped("720p", ignore.skipped_keywords)
    assert not should_be_skipped("1080p", ignore.skipped_keywords)
