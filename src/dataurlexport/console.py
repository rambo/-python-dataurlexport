"""CLI entrypoints for dataurlexport"""

import logging
from pathlib import Path

import click

from libadvian.logging import init_logging
from dataurlexport import __version__
from dataurlexport.exporter import Exporter


LOGGER = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__)
@click.option("-l", "--loglevel", help="Python log level, 10=DEBUG, 20=INFO, 30=WARNING, 40=CRITICAL", default=30)
@click.option("-v", "--verbose", count=True, help="Shorthand for info/debug loglevel (-v/-vv)")
@click.argument("filepath", type=click.Path())
@click.argument("prefix")
def dataurlexport_cli(loglevel: int, verbose: int, filepath: str | Path, prefix: str) -> None:
    """Post-process RUNE outputs and export data urls as files"""
    if verbose == 1:
        loglevel = 20
    if verbose >= 2:
        loglevel = 10
    init_logging(loglevel)
    LOGGER.setLevel(loglevel)
    exp = Exporter(Path(filepath), prefix)
    exp.process()
