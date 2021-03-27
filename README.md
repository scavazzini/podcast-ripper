# Podcast Ripper

Command line software to download podcast episodes.

# Installation

```bash
git clone https://github.com/scavazzini/podcast-ripper.git
cd podcast-ripper
python3 setup.py install
```

# Usage

## Download all episodes

```bash
podcast-ripper download [OPTIONS] FEED_URL [DESTINATION]
```

**FEED_URL** can be a RSS Feed or an OPML file.

Options:
  - ```--max-episodes INTEGER```: Limit of episodes to be downloaded.
