import json
from apiclient import discovery
from utils import get_random_element_from_list


def retrieve_videos(req):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    google_api_key, channel_id = __parse(req)

    API_VER = "v3"
    youtube_service = discovery.build("youtube", API_VER, developerKey=google_api_key)

    videos = []
    next_page_token = None

    while True:
        req = youtube_service.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,  # 1回のリクエストで取得する最大動画数
            pageToken=next_page_token,
        )

        # チャンネル内の全てのビデオ
        res = req.execute()

        for item in res["items"]:
            if __is_want_share_video(item):
                video_id = item["id"]["videoId"]
                title = __get_video_title_by_id(youtube_service, video_id)
                videos.append(
                    {
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "title": title,
                    }
                )

        next_page_token = res.get("nextPageToken")

        if not next_page_token:
            break

    NUM_OF_RETRIEVE_VIDEOS = 3
    videos = get_random_element_from_list(videos, NUM_OF_RETRIEVE_VIDEOS)

    return json.dumps(videos)


def __parse(req):
    req_json = req.get_json()
    GOOGLE_API_KEY = req_json["google_api_key"]
    channel_id = req_json["channel_id"]
    return GOOGLE_API_KEY, channel_id


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
