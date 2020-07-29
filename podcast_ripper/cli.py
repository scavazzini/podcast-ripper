import os
import click
import humanize
from slug import slug

import podcast_ripper


@click.group()
@click.version_option(version=podcast_ripper.__version__, prog_name="Podcast Ripper")
def cli():
    pass

if __name__ == "__main__":
    cli()
