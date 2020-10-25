import os

import Crowbars
import Panopto
from CS390 import CS390
from CS453 import CS453
from CS488 import CS488
from CS490 import CS490
from CS499 import CS499

def start_parsing(session):
    classes = [
        CS390(),
        CS453(),
        CS488(),
        CS490(),
        CS499()
    ]

    for cs_class in classes:
        class_name = cs_class.name
        existing_guids = Crowbars.get_existing_guids(class_name)

        for video in cs_class.videos:
            video_url = video["id"]

            if video_url not in existing_guids:
                Crowbars.log("Found new video: [" + class_name + "] " + video["title"])
                Crowbars.log("Making crawl job...")
                crawl_job = Crowbars.make_crawl_job(session, video, class_name)
                Crowbars.log("Saving crawl job...")
                Crowbars.save_crawl_job(crawl_job, video_url, class_name)
                Crowbars.log("Marking as processed...")
                Crowbars.save_guid(class_name, video_url)
                Crowbars.log("Done.")

session = Panopto.perform_sso_login(os.environ["PANOPTOSYNC_SSO_USERNAME"], os.environ["PANOPTOSYNC_SSO_PASSWORD"])
start_parsing(session)
