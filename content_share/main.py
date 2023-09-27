import tweepy
from dotenv import load_dotenv
import os
import base64
from apiclient.discovery import build
import logging

import requests
import json
import sys

"""Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """


# TODO: GCP Pub / Sub エミュレータ
# def main():
def main(event, context):
    try:
        load_dotenv()
        # TODO: cloud schedulerからシェアするコンテンツの情報をjsonなどで受け取る
        # __do_tweet()

        __my_movies()
        __notify_to_slack()
        return "Hello {}!!Q".format("name")

        # pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        # print(pubsub_message)
        # print(f"context is {context}")

    except Exception as e:
        e_type, e_value, e_traceback = sys.exc_info()
        logging.error("Exception type : %s " % e_type.__name__)
        logging.error("Exception message : %s " % e_value.__name__)
        logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e


def __notify_to_slack():
    payload = {
        "icon_emoji": ":ghost:",
        "username": "new-bot-name",
        "text": "定期実行処理が完了しました",
    }

    headers = {"Content-Type": "application/json; charset=UTF-8"}
    res = requests.post(
        url=os.getenv("SLACK_WEBHOOK_URL"),
        headers=headers,
        data=json.dumps(payload),
        proxies=None,
    )
    print(res)


def __do_tweet() -> None:
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )
    client.create_tweet(
        text="【Genie AI】VSCodeにインストールすべきChatGPT拡張\n\nhttps://www.youtube.com/watch?v=ngLbfn_3KfQ&feature=youtu.be\n\n#ChatGPt"
    )


def __my_movies():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    API_VER = "v3"
    youtube = build("youtube", API_VER, developerKey=GOOGLE_API_KEY)

    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id",
            channelId="UC5AcEeC1LjJ7f5-o5jxfzqQ",
            maxResults=50,  # 1回のリクエストで取得する最大動画数
            pageToken=next_page_token,
        )

        # チャンネル内の全てのビデオ
        response = request.execute()

        for item in response["items"]:
            if is_want_share_video(item):
                video_id = item["id"]["videoId"]

                # ビデオIDに一致するビデオ
                res = (
                    youtube.videos()
                    .list(part="snippet,statistics", id="{},".format(video_id))
                    .execute()
                )

                snippetInfo = res["items"][0]["snippet"]
                title = snippetInfo["title"]
                videos.append({"id": video_id, "title": title})

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    print("チャンネルの動画一覧:")
    for video_info in videos:
        print(
            f"Url: https://www.youtube.com/watch?v={video_info['id']}, title: {video_info['title']}"
        )


def is_want_share_video(item) -> bool:
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


# if __name__ == "__main__":
#     main()
