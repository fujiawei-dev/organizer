"""Console script for organizer."""

import sys

import click

from organizer import __version__
from organizer.config.settings import Settings
from organizer.runner.carry import carry_tv


@click.command(help="Organize your TV Shows.")
@click.option("--version", "-v", is_flag=True, help="Print the version of organizer.")
@click.option("--config-file", "-c", type=str, default="config.yml")
def main(version: bool, config_file: str):
    if version:
        click.echo(__version__)
        return

    settings = Settings(config_file=config_file)

    carry_tv(
        settings.src,
        settings.dst,
        settings.ignore,
        settings.tmdb.api_key,
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
