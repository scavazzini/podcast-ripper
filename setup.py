from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='podcast_ripper',
   version='0.0.1dev',
   author='Newton Scavazzini',
   description='A podcast ripper',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/scavazzini/podcast-ripper/",
   packages=['podcast_ripper'],
   install_requires=[
       'podcastparser',
       'requests',
       'click',
       'slug',
       'humanize',
   ],
    entry_points={
        "console_scripts": [
            "podcast-ripper = podcast_ripper.cli:cli"
        ]
    },
)
