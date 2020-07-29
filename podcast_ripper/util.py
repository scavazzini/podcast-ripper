import podcastparser
from urllib.request import urlopen, Request

import podcast_ripper


def parse(url, max_episodes):

    req = Request(url, headers={'User-Agent': podcast_ripper.__user_agent__})
    parsed = podcastparser.parse(url, urlopen(req), max_episodes)

    podcast = podcast_ripper.Podcast(parsed['title'], parsed['link'])

    for episode in parsed['episodes']:
        episode = podcast_ripper.Episode(episode['title'], episode['published'], episode['enclosures'][0]['url'])
        podcast.episodes.append(episode)

    return podcast
