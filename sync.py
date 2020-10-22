import os
from datetime import datetime

from Panopto import Panopto
from Common import Common
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
        existing_guids = Common.get_existing_guids(class_name)

        for video in cs_class.videos:
            video_url = video["id"]

            if video_url not in existing_guids:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Adding new video: [" + class_name + "] " + video["title"])
                crawl_job = Common.make_crawl_job(session, video, class_name)
                Common.save_crawl_job(crawl_job, video_url, class_name)
                Common.save_guid(class_name, video_url)

session = Panopto.perform_sso_login(os.environ["PANOPTOSYNC_SSO_USERNAME"], os.environ["PANOPTOSYNC_SSO_PASSWORD"])
start_parsing(session)
