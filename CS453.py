import feedparser
from os import environ
from Common import Common

class CS453:

    name = "CS 453"
    videos = {}

    def __init__(self):
        feed_data = feedparser.parse(environ["PANOPTOSYNC_CS453_FEED"])

        counter = 0
        for i, entry in enumerate(feed_data.entries):
            counter = counter + 1

            title = entry["title"]
            title = Common.remove_prefix(title, "CS 453: ")
            title = title.strip()

            feed_data.entries[i]["title"] = str(counter) + " - " + title

        self.videos = feed_data.entries


