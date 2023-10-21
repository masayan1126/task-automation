import os
from apiclient import discovery
from utils import get_random_element_from_list


# 参考：https://zenn.dev/eito_blog/articles/94dc874c112c9f
def retrieve_want_to_share_videos(num_of_retrieve_videos: int) -> list:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    API_VER = "v3"
    youtube_service = discovery.build("youtube", API_VER, developerKey=GOOGLE_API_KEY)

    videos = []
    next_page_token = None

    while True:
        request = youtube_service.search().list(
            part="id",
            channelId="UC5AcEeC1LjJ7f5-o5jxfzqQ",
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

    return get_random_element_from_list(videos, num_of_retrieve_videos)


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
