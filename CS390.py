import feedparser
from os import environ
from Common import Common

class CS390:

    name = "CS 390"
    videos = {}

    def __init__(self):
        feed_data = feedparser.parse(environ["PANOPTOSYNC_CS390_FEED"])

        counter = 0
        for i, entry in enumerate(feed_data.entries):
            counter = counter + 1

            title = entry["title"]
            title = Common.remove_prefix(title, "CS 390: ")
            title = Common.remove_prefix(title, "CS390-")
            title = title.strip()

            feed_data.entries[i]["title"] = str(counter) + " - " + title

        self.videos = feed_data.entries


