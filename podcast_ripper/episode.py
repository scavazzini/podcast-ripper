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

        if not os.path.exists(location):
            os.makedirs(location)

        path = os.path.join(location, self.filename)
        downloaded = 0

        with requests.get(self.file_url, timeout=5, stream=True,
                          headers={"User-Agent": podcast_ripper.__user_agent__}) as r:

            r.raise_for_status()

            try:
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)

            except BaseException as e:
                if os.path.exists(path):
                    os.remove(path)
                raise e

        return downloaded

    @property
    # TODO: Detect file extension correctly.
    def filename(self):
        return "{}-{}.{}".format(self.published, slug(self.title), self.extension)

    @property
    def extension(self):
        return self.file_url.split('.')[-1].lower()
