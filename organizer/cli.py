"""Console script for organizer."""
import os
import sys

import click
from toolkit.config.runtime import EDITOR

from organizer import __version__
from organizer.config import DEFAULT_CONFIG_FILE
from organizer.config.settings import Settings
from organizer.runner.carry import carry_tv


@click.command(help="Organize your TV Shows.")
@click.option("--version", "-v", is_flag=True, help="Print the version of organizer.")
@click.option(
    "--config-file",
    "-c",
    type=str,
    default=DEFAULT_CONFIG_FILE,
    help="Path to the config file.",
)
@click.option("--edit-config-file", "-e", is_flag=True, help="Edit the config file.")
@click.option(
    "--open-source-directory",
    "-s",
    is_flag=True,
    help="Open the source directory.",
)
@click.option(
    "--open-destination-directory",
    "-d",
    is_flag=True,
    help="Open the destination directory.",
)
def main(
    version: bool,
    config_file: str,
    edit_config_file: bool,
    open_source_directory: bool,
    open_destination_directory: bool,
):
    if version:
        click.echo(__version__)
        return

    config_file = os.path.expanduser(config_file)

    if edit_config_file:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        click.edit(filename=config_file, editor=EDITOR)
        return

    settings = Settings(config_file=config_file)

    if open_source_directory:
        click.echo('Opening "{}"'.format(settings.src))
        click.launch(settings.src, locate=True)
        return

    if open_destination_directory:
        click.echo('Opening "{}"'.format(settings.dst))
        click.launch(settings.dst, locate=True)
        return

    carry_tv(
        settings.src,
        settings.dst,
        settings.ignore,
        settings.tmdb.api_key,
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
