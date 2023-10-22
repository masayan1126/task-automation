import json
import os
from dotenv import load_dotenv
import requests
import google.auth.transport.requests
import google.oauth2.id_token


# 参考：https://zenn.dev/eito_blog/articles/94dc874c112c9f
def main(event=None, context=None):
    load_dotenv()

    share_content_list = retrieve_video_list()

    video_list = share_to_x(share_content_list)


def retrieve_video_list() -> list:
    youtube_video_retrieve_service_endpoint = "https://asia-northeast1-masayan1126.cloudfunctions.net/youtube_video_retrieve_service"
    youtube_video_retrieve_service_id_token = get_token(
        youtube_video_retrieve_service_endpoint
    )

    headers = {
        "Authorization": f"Bearer {youtube_video_retrieve_service_id_token}",
        "Content-Type": "application/json",
    }

    data = {
        # "AIzaSyDujSCmj2xcx_620BeN2aSX140XmcP-5A0"
        "google_api_key": os.environ["GOOGLE_API_KEY"],
        # "UC5AcEeC1LjJ7f5-o5jxfzqQ"
        "channel_id": os.environ["YOUTUBE_CHANNEL_ID"],
    }

    res = requests.post(
        url=youtube_video_retrieve_service_endpoint,
        headers=headers,
        data=json.dumps(data),
    )

    video_list = json.loads(res.content)

    return video_list


def share_to_x(share_content_list: list) -> list:
    x_share_service_endpoint = (
        "https://asia-northeast1-masayan1126.cloudfunctions.net/x_share_service"
    )
    x_share_service_endpoint_id_token = get_token(x_share_service_endpoint)

    headers = {
        "Authorization": f"Bearer {x_share_service_endpoint_id_token}",
        "Content-Type": "application/json",
    }

    data = {"share_content_list": share_content_list}

    res = requests.post(
        url=x_share_service_endpoint,
        headers=headers,
        data=json.dumps(data),
    )

    print(res.content, flush=True)

    # video_list = json.loads(res.content)

    return [""]


def get_token(service_endpoint: str) -> str:
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(
        auth_req,
        service_endpoint,
    )

    return id_token
