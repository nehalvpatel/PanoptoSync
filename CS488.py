import feedparser
from os import environ
from Common import Common

class CS488:

    name = "CS 488"
    videos = {}

    def __init__(self):
        feed_data = feedparser.parse(environ["PANOPTOSYNC_CS488_FEED"])

        counter = 0
        for i, entry in enumerate(feed_data.entries):
            counter = counter + 1

            title = entry["title"]
            title = Common.remove_prefix(title, "CS 488: ")
            title = Common.remove_prefix(title, "(CS 488-01)")
            title = title.strip()
            title = Common.remove_prefix(title, "(FA20)")
            title = title.strip()
            title = Common.remove_prefix(title, "-")
            title = title.strip()
            title = Common.remove_prefix(title, "CS488")
            title = Common.remove_prefix(title, "CS 488")
            title = title.strip()
            title = Common.remove_prefix(title, "-")
            title = title.strip()

            feed_data.entries[i]["title"] = str(counter) + " - " + title

        self.videos = feed_data.entries


