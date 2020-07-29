import os
import textwrap

import click
import humanize
from slug import slug

import podcast_ripper


def progress_callback(current, total, message):
    w = len(str(total))
    print(" [{0:{w}d}/{1}] {2}".format(current, total, message, w=w))


@click.group()
@click.version_option(version=podcast_ripper.__version__, prog_name="Podcast Ripper")
def cli():
    pass


@cli.command(help='Download episodes')
@click.option("--max-episodes", type=int)
@click.argument('feed_url')
@click.argument('destination', required=False)
def download(feed_url, destination, max_episodes):
    """Download episodes"""

    feeds = [feed_url]
    destination = destination or ''
    downloaded = 0

    try:

        for feed in feeds:

            print()
            print('Fetching feed...')
            podcast = podcast_ripper.parse(feed, max_episodes)
            download_dir = os.path.join(destination, slug(podcast.name))

            print_header = '''
            {name} ({url})
            {episodes} episodes to download

            Starting download...
            '''.format(name=podcast.name, url=podcast.url, episodes=len(podcast.episodes))

            print(textwrap.dedent(print_header))

            downloaded += podcast.download(download_dir, progress_callback)

    except KeyboardInterrupt:
        print()
        print("Aborted. {} downloaded.".format(humanize.naturalsize(downloaded)))
        exit()

    print()
    print("Completed. {} downloaded.".format(humanize.naturalsize(downloaded)))
    print()


@cli.command(help='Print episodes urls')
@click.option("--max-episodes", type=int)
@click.argument('feed_url')
def dump_urls(feed_url, max_episodes):

    podcast = podcast_ripper.parse(feed_url, max_episodes)

    for episode in podcast.episodes:
        print(episode.file_url)

if __name__ == "__main__":
    cli()
