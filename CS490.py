import feedparser
from os import environ
import Crowbars

class CS490:

    name = "CS 490"
    videos = {}

    def __init__(self):
        feed_data1 = feedparser.parse(environ["PANOPTOSYNC_CS490A_FEED"])
        feed_data2 = feedparser.parse(environ["PANOPTOSYNC_CS490B_FEED"])

        self.videos = feed_data1.entries + feed_data2.entries

        self.videos = sorted(self.videos, key = lambda video: video["title"])
        self.videos = sorted(self.videos, key = lambda video: video["published_parsed"])

        counter = 0
        for i, video in enumerate(self.videos):
            counter = counter + 1

            title = video["title"]
            title = Crowbars.remove_prefix(title, "CS 490: ")
            title = Crowbars.remove_prefix(title, "CS490")
            title = title.strip()

            self.videos[i]["title"] = str(counter) + " - " + title







