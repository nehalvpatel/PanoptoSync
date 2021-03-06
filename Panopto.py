import requests
import m3u8
import urllib.parse as urlparse
from os import environ
from bs4 import BeautifulSoup
from urllib.parse import parse_qs

import Crowbars

def parse_panopto_delivery_id(panopto_url):
    parsed = urlparse.urlparse(panopto_url)
    return parse_qs(parsed.query)['id'][0]

def fetch_sso_execution(session):
    sso_response = session.get(environ["PANOPTOSYNC_SSO_URL"])
    soup = BeautifulSoup(sso_response.text, 'html.parser')

    execution_input = soup.find(attrs={"name": "execution"})
    return execution_input["value"]

def perform_sso_login(username, password):
    session = requests.session()
    session.post(environ["PANOPTOSYNC_SSO_URL"], {
        "username": username,
        "password": password,
        "execution": fetch_sso_execution(session),
        "_eventId": "submit",
        "geolocation": ""
    })
    return session

def fetch_panopto_csrf(session, panopto_url):
    panopto_response = session.get(panopto_url)
    soup = BeautifulSoup(panopto_response.text, 'html.parser')

    csrf_input = soup.find(attrs={"name": "panoptoProtectionToken" })
    return csrf_input["value"]

def get_video_audio_streams(session, stream_urls):
    audio_url = ""
    video_url = ""

    first_url = stream_urls[0]
    second_url = stream_urls[1]

    first_feed = m3u8.load(first_url)
    second_feed = m3u8.load(second_url)

    for playlist in first_feed.playlists:
        if playlist.stream_info.resolution is None:
            audio_url = playlist.base_uri + playlist.uri
            video_url = get_best_stream_url(session, [second_url])
            break

    for playlist in second_feed.playlists:
        if playlist.stream_info.resolution is None:
            audio_url = playlist.base_uri + playlist.uri
            video_url = get_best_stream_url(session, [first_url])
            break

    return (video_url, audio_url)

def get_best_stream_url(session, stream_urls):
    if (len(stream_urls) == 0):
        Crowbars.log("No stream URLs found...")
        return ""
    elif (len(stream_urls) == 1):
        Crowbars.log("Fetching playlist [" + stream_urls[0] + "]...")

        if "master.m3u8" not in stream_urls[0]:
            Crowbars.log("Stream URL is actually a video file. We'll download it directly...")
            return stream_urls[0]

        m3u8_response = session.get(stream_urls[0], timeout=30)
        Crowbars.log("Received M3U8 playlist. Parsing...")
        playlist = m3u8.loads(m3u8_response.text, stream_urls[0])

        if not playlist.is_variant:
            return stream_urls[0]
        else:
            max_res = 0
            max_res_url = ""

            for var_playlist in playlist.playlists:
                if var_playlist.stream_info.resolution[0] > max_res:
                    max_res = var_playlist.stream_info.resolution[0]
                    max_res_url = var_playlist.base_uri + var_playlist.uri

            return max_res_url

def fetch_stream_urls(session, viewer_url):
    delivery_id = parse_panopto_delivery_id(viewer_url)
    csrf_token = fetch_panopto_csrf(session, "https://" + environ["PANOPTOSYNC_PANOPTO_DOMAIN"] + "/Panopto/Pages/Viewer.aspx?id=" + delivery_id)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Pragma': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': environ["PANOPTOSYNC_PANOPTO_DOMAIN"],
        'Origin': 'https://' + environ["PANOPTOSYNC_PANOPTO_DOMAIN"],
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Referer': "https://" + environ["PANOPTOSYNC_PANOPTO_DOMAIN"] + "/Panopto/Pages/Viewer.aspx?id=" + delivery_id,
        'Connection': 'keep-alive',
        'x-requested-with': 'XMLHttpRequest',
        'x-csrf-token': csrf_token,
    }

    data = {
        'deliveryId': delivery_id,
        'invocationId': '',
        'isLiveNotes': 'false',
        'refreshAuthCookie': 'true',
        'isActiveBroadcast': 'false',
        'isEditing': 'false',
        'isKollectiveAgentInstalled': 'false',
        'isEmbed': 'false',
        'responseType': 'json'
    }

    response = session.post('https://' + environ["PANOPTOSYNC_PANOPTO_DOMAIN"] + '/Panopto/Pages/Viewer/DeliveryInfo.aspx', headers=headers, data=data).json()

    streams = response["Delivery"]["Streams"]

    stream_urls = []
    for stream in streams:
        stream_urls.append(stream["StreamUrl"])

    return stream_urls
