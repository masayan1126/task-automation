import tweepy
from dotenv import load_dotenv
import os
import base64
from apiclient.discovery import build

import requests
import json

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

        # __my_movies()

        # pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        # print(pubsub_message)

        __notify_to_slack()

        # print(f"context is {context}")
        return "Hello {}!!Q".format("name")
    except Exception as e:
        print(f"Exception is {e}")


def __notify_to_slack():
    payload = {
        "icon_emoji": ":ghost:",
        "username": "new-bot-name",
        "text": "定期実行処理が完了しました",
    }

    headers = {"Content-Type": "application/json; charset=UTF-8"}
    res = requests.post(
        "https://hooks.slack.com/services/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",
        headers=headers,
        data=json.dumps(payload),
        proxies=None,
    )
    raise print(res)


def __create_client() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )


def __do_tweet() -> None:
    client = __create_client()
    client.create_tweet(
        text="【Genie AI】VSCodeにインストールすべきChatGPT拡張\n\nhttps://www.youtube.com/watch?v=ngLbfn_3KfQ&feature=youtu.be\n\n#ChatGPt"
    )


def __my_movies():
    API_KEY = os.getenv("API_KEY")
    API_VER = "v3"
    youtube = build("youtube", API_VER, developerKey=API_KEY)
    channel_id = "UC5AcEeC1LjJ7f5-o5jxfzqQ"

    channel = (
        youtube.channels().list(part="snippet,contentDetails", id=channel_id).execute()
    )
    item = channel["items"]
    print(f"My channel is ={item}")


# if __name__ == "__main__":
#     main()
