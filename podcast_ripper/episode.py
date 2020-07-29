import os

import requests
from slug import slug

import podcast_ripper


class Episode:

    def __init__(self, title, published, file_url):
        self.title = title
        self.published = published
        self.file_url = file_url

    def download(self, location):

        request = requests.get(self.file_url, headers={"User-Agent": podcast_ripper.__user_agent__})
        content = request.content

        if not os.path.exists(location):
            os.makedirs(location)

        path = os.path.join(location, self.filename)

        with open(path, 'wb') as f:
            f.write(content)

        return len(content)

    @property
    def filename(self):
        return "{}-{}.{}".format(self.published, slug(self.title), self.extension)

    @property
    def extension(self):
        return self.file_url.split('.')[-1].lower()
