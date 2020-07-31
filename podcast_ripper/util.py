import podcastparser
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET

import podcast_ripper


def parse(url, max_episodes=0):

    with getfile(url) as file:

        parsed = podcastparser.parse(url, file, max_episodes)

        podcast = podcast_ripper.Podcast(parsed.get('title', 'Unknown'),
                                         parsed.get('link', ''),
                                         parsed.get('description', ''))

        for episode in parsed['episodes']:
            if len(episode['enclosures']) > 0:
                episode = podcast_ripper.Episode(episode['title'], episode['published'], episode['enclosures'][0]['url'])
                podcast.episodes.append(episode)

    return podcast


def get_feeds_from_opml(uri):

    with getfile(uri) as opml_file:

        root = ET.parse(opml_file).getroot()

        feeds = []
        for element in root.iter():

            if element.get('type') != 'rss' and element.get('type') != 'link':
                continue

            feed_url = element.get('xmlUrl') or element.get('url')

            if feed_url is None:
                continue

            feeds.append(feed_url)

    return feeds


def getfile(uri):

    if uri.lower().startswith('http://') or uri.lower().startswith('https://'):
        req = Request(uri, headers={'User-Agent': podcast_ripper.__user_agent__})
        return urlopen(req)

    return open(uri, 'rb')
