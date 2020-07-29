import os
import click
import humanize
from slug import slug

import podcast_ripper


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

    print('Fetching feed...')

    podcast = podcast_ripper.parse(feed_url, max_episodes)
    download_dir = os.path.join(destination or '', slug(podcast.name))

    print()
    print("{} ({})".format(podcast.name, podcast.url))
    print("{} episodes to download".format(len(podcast.episodes)))
    print()

    print('Starting download')

    downloaded = 0
    w = len(str(len(podcast.episodes)))

    try:

        for i, episode in enumerate(podcast.episodes, 1):

            if os.path.exists(os.path.join(download_dir, episode.filename)):
                print(" [{0:{w}d}/{1}] {2} already exists".format(i, len(podcast.episodes), episode.filename, w=w))
                continue

            print(" [{0:{w}d}/{1}] Downloading {2}".format(i, len(podcast.episodes), episode.filename, w=w))
            downloaded += episode.download(download_dir)

    except KeyboardInterrupt:
        print()
        print("Aborted. {} downloaded.".format(humanize.naturalsize(downloaded)))
        exit()

    print()
    print("Completed. {} downloaded.".format(humanize.naturalsize(downloaded)))


if __name__ == "__main__":
    cli()
