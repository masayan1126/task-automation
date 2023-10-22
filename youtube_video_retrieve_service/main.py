import json

# import os
from apiclient import discovery
import flask
from utils import get_random_element_from_list
from dotenv import load_dotenv


def retrieve_videos(request: flask.Request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    print(request_json["google_api_key"], flush=True)

    load_dotenv()
    # destination_topic = base64.b64decode(event["data"]).decode("utf-8")

    num_of_retrieve_videos = 3
    GOOGLE_API_KEY = request_json["google_api_key"]
    API_VER = "v3"
    youtube_service = discovery.build("youtube", API_VER, developerKey=GOOGLE_API_KEY)

    videos = []
    next_page_token = None

    # d = {
    #     "google_api_key": "masayan1126-o5jxfzqQ",
    #     "channel_id": "UC5AcEeC1LjJ7f5-o5jxfzqQ",
    # }

    while True:
        request = youtube_service.search().list(
            part="id",
            channelId=request_json["channel_id"],
            maxResults=50,  # 1回のリクエストで取得する最大動画数
            pageToken=next_page_token,
        )

        # チャンネル内の全てのビデオ
        response = request.execute()

        for item in response["items"]:
            if __is_want_share_video(item):
                video_id = item["id"]["videoId"]
                title = __get_video_title_by_id(youtube_service, video_id)
                videos.append(
                    {
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "title": title,
                    }
                )

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    videos = get_random_element_from_list(videos, num_of_retrieve_videos)

    return json.dumps(videos)

    # publisher = pubsub_v1.PublisherClient()
    # topic_path = publisher.topic_path(
    #     os.environ.get("GCP_PROJECT_ID", ""), topic=destination_topic
    # )

    # data = json.dumps(videos_).encode("utf-8")
    # print(f"destination_topic={destination_topic}")
    # print(f"topic_path={topic_path}")

    # future = publisher.publish(topic_path, data)


def __get_video_title_by_id(youtube_service, video_id: str) -> str:
    # ビデオIDに一致するビデオ
    res = (
        youtube_service.videos()
        .list(part="snippet,statistics", id="{},".format(video_id))
        .execute()
    )

    snippetInfo = res["items"][0]["snippet"]
    title = snippetInfo["title"]
    return title


def __is_want_share_video(item) -> bool:
    exclude_video_ids = [
        # エンジニアリング以外
        "a9UJ99caBTQ",
        "Z2Dn6Xtqb6I",
        "7FTjlE7FYZ8",
        "9xo4ChsAGes",
        "c9hQhKth8iU",
        "40GWEutdMpg",
        "JhGZdJDKBgk",
        "q-LdsnYdYmc",
        "7jYfbwp5-RE",
        # 【プログラミング】Reactにtailwindcssを導入する
        "mvu1G2I32nzfLlAV",
        # webpack関連3つ
        "wV-R1DM59kkJqGsB",
        "z3cm601dfTUF4VW_",
        "QJIbIpY5ZD7zGoKA",
    ]

    return (
        item["id"]["kind"] == "youtube#video"
        and item["id"]["videoId"] not in exclude_video_ids
    )
