import json
from os import environ, path

from Panopto import Panopto

class Common:
    @staticmethod
    def remove_prefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text  # or whatever

    @staticmethod
    def make_crawl_job_object(stream_url, class_name, video_title, filename, auto_start, auto_confirm):
        return {
            "downloadFolder": environ["PANOPTOSYNC_DOWNLOAD_FOLDER"] + class_name,
            "chunks": 0,
            "overwritePackagizerEnabled" : True,
            "extractAfterDownload" : "UNSET",
            "priority" : None,
            "type" : "NORMAL",
            "enabled" : "TRUE",
            "autoStart" : auto_start,
            "autoConfirm" : auto_confirm,
            "forcedStart" : "UNSET",
            "addOfflineLink" : True,
            "extractPasswords" : None,
            "downloadPassword" : None,
            "comment" : None,
            "text" : stream_url,
            "filename" : filename,
            "packageName" : video_title,
            "deepAnalyseEnabled" : False,
            "setBeforePackagizerEnabled" : False
        }

    @staticmethod
    def make_crawl_job(s, video, class_name):
        stream_urls = Panopto.fetch_stream_urls(s, video["id"])

        if len(stream_urls) == 1:
            stream_url_string = Panopto.get_best_stream_url(stream_urls)
            filename = video["title"] + ".mp4"
            auto_start = "TRUE"
            auto_confirm = "TRUE"

            return [Common.make_crawl_job_object(stream_url_string, class_name, video["title"], filename, auto_start, auto_confirm)]
        elif len(stream_urls) == 2:
            av_pair = Panopto.get_video_audio_streams(stream_urls)
            auto_start = "TRUE"
            auto_confirm = "TRUE"

            return [
                Common.make_crawl_job_object(av_pair[0], class_name, video["title"] + " (TOMERGE)", video["title"] + "__TOMERGE.mp4", auto_start, auto_confirm),
                Common.make_crawl_job_object(av_pair[1], class_name, video["title"] + " (TOMERGE)", video["title"] + "__TOMERGE.m4a", auto_start, auto_confirm)
            ]
        else:
            raise Exception("More than 2 stream URLs discovered")

    @staticmethod
    def get_existing_guids(class_name):
        guid_path = "./" + class_name.replace(" ", "") + ".txt"
        existing_guids = []

        if path.exists(guid_path):
            with open(guid_path, 'r') as file:
                existing_guid = file.read()
                existing_guids = existing_guid.splitlines()
        else:
            raise Exception("GUID file not found")

        return existing_guids

    @staticmethod
    def save_guid(class_name, guid):
        guid_path = "./" + class_name.replace(" ", "") + ".txt"
        with open(guid_path, 'a') as file:
            guid = guid.strip()
            guid = "\n" + guid
            file.write(guid)

    @staticmethod
    def save_crawl_job(crawl_job, video_id, class_name):
        with open(environ["PANOPTOSYNC_CRAWLJOB_FOLDER"] + class_name.replace(" ", "") + "_" + str(hash(video_id)) + ".crawljob", "w") as file:
            file.write(json.dumps(crawl_job, sort_keys=True, indent=4))
