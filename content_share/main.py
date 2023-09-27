import tweepy
from dotenv import load_dotenv
import os
import base64

import logging


import sys

from notification import notify_to_slack
from youtube import my_videos

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

        videos = my_videos()

        print("チャンネルの動画一覧:")
        for video_info in videos:
            print(f"url: {video_info['url']}, title: {video_info['title']}")

        res = notify_to_slack()
        print(f"Notification response={res}")

        # TODO: 動画リストからランダムに2つシェア
        # TODO: プログ記事も追加する

        # __do_tweet()

        # pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        # print(pubsub_message)
        # print(f"context is {context}")

    except Exception as e:
        e_type, e_value, e_traceback = sys.exc_info()
        logging.error("Exception type : %s " % e_type.__name__)
        logging.error("Exception message : %s " % e_value.__name__)
        logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e


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


# if __name__ == "__main__":
#     main()
