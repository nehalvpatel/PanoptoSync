import feedparser
from os import environ
import Crowbars

class CS499:

    name = "CS 499"
    videos = {}

    def __init__(self):
        feed_data = feedparser.parse(environ["PANOPTOSYNC_CS499_FEED"])

        counter = 0
        for i, entry in enumerate(feed_data.entries):
            counter = counter + 1

            title = entry["title"]
            title = Crowbars.remove_prefix(title, "CS 499: ")
            title = title.replace("CS 499 ", "")
            title = title.replace("CS 499", "")
            title = title.strip()

            feed_data.entries[i]["title"] = str(counter) + " - " + title

        self.videos = feed_data.entries


