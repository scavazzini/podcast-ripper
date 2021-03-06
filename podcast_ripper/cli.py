import os
import textwrap

import click
import humanize
from podcastparser import FeedParseError
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

    podcasts = []

    try:
        podcast = podcast_ripper.parse(feed_url, max_episodes)
        podcasts.append(podcast)

    except FeedParseError as exception:

        if exception.getMessage() != 'Unsupported feed type: opml':
            print('Failed to parse your feed: {}'.format(exception.getMessage()))
            exit()

        # Feed is a OPML file, try to parse
        try:

            feeds = podcast_ripper.get_feeds_from_opml(feed_url)
            if isinstance(feeds, list) and len(feeds) > 0:

                print("OPML with {} feeds found".format(len(feeds)))

                for feed in feeds:
                    print('Parsing {}'.format(feed))
                    podcasts.append(podcast_ripper.parse(feed, max_episodes))

        except Exception as exception:
            print()
            print('Failed to parse your OPML: {}'.format(str(exception)))
            exit()

    except Exception as exception:
        print()
        print('Failed to parse your feed: {}'.format(exception))
        exit()

    destination = destination or ''
    downloaded = 0

    for podcast in podcasts:

        download_dir = os.path.join(destination, slug(podcast.name))

        print_header = '''
        {name} ({url})
        {episodes} episodes to download

        Starting download...
        '''.format(name=podcast.name, url=podcast.url, episodes=len(podcast.episodes))

        print(textwrap.dedent(print_header))

        downloaded += podcast.download(download_dir, progress_callback)

    print()
    print("Completed. {} downloaded.".format(humanize.naturalsize(downloaded)))
    print()


@cli.command(help='Show podcast information')
@click.argument('feed_url')
def show(feed_url):

    podcast = podcast_ripper.parse(feed_url)

    print('Name: {}'.format(podcast.name))
    print('URL: {}'.format(podcast.url))
    print('Description: {}'.format(podcast.description))
    print('Episodes: {}'.format(len(podcast.episodes)))


@cli.command(help='Print episodes urls')
@click.option("--max-episodes", type=int)
@click.argument('feed_url')
def dump_urls(feed_url, max_episodes):

    podcast = podcast_ripper.parse(feed_url, max_episodes)

    for episode in podcast.episodes:
        print(episode.file_url)


if __name__ == "__main__":
    cli()
