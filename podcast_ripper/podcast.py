import os


class Podcast:

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.episodes = []

    def download(self, download_dir, _callback=None):

        downloaded = 0

        for i, episode in enumerate(self.episodes, 1):

            if os.path.exists(os.path.join(download_dir, episode.filename)):
                if _callback:
                    _callback(i, len(self.episodes), "{} already exists".format(episode.filename))
                continue

            if _callback:
                _callback(i, len(self.episodes), "Downloading {}".format(episode.filename))

            downloaded += episode.download(download_dir)

        return downloaded
