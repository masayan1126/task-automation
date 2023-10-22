import json
import os
from dotenv import load_dotenv
import requests
import google.auth.transport.requests
import google.oauth2.id_token


# 参考：https://zenn.dev/eito_blog/articles/94dc874c112c9f
def main(event=None, context=None):
    load_dotenv()

    share_video_list = retrieve_video_list()
    shared_videos = share_to_x(share_video_list)

    res = notify_to_slack(
        payload={
            "icon_emoji": ":ghost:",
            "username": "new-bot-name",
            "text": f"定期シェア処理が完了しました\n\n{shared_videos}",
        },
        to=os.getenv("SLACK_WEBHOOK_URL", ""),
    )
    print(f"Notification response={res}")


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
        "google_api_key": os.environ["GOOGLE_API_KEY"],
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

    video_list = json.loads(res.content)

    return video_list


def get_token(service_endpoint: str) -> str:
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(
        auth_req,
        service_endpoint,
    )

    return id_token


def notify_to_slack(payload: dict, to: str) -> requests.Response:
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    res = requests.post(
        url=to,
        headers=headers,
        data=json.dumps(payload),
        proxies=None,
    )

    return res
