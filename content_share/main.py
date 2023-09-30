import os
from utils import get_random_element_from_list
from x import do_tweet
from dotenv import load_dotenv
import logging
import sys
from youtube import my_videos
from x import do_tweet
from taopypy.notification import notify_to_slack

"""Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """


def main(event, context):
    try:
        load_dotenv()
        # TODO: cloud schedulerからシェアするコンテンツの情報をjsonなどで受け取る

        videos = my_videos()

        print("チャンネルの動画一覧:")
        for video_info in videos:
            print(f"url: {video_info['url']}, title: {video_info['title']}")

        share_content_list = get_random_element_from_list(videos, 2)
        # TODO: プログ記事も追加する
        # TODO: logをutil化する

        do_tweet(share_content_list)

        res = notify_to_slack(
            payload={
                "icon_emoji": ":ghost:",
                "username": "new-bot-name",
                "text": f"定期シェア処理が完了しました\n\n{share_content_list}",
            },
            to=os.getenv("SLACK_WEBHOOK_URL"),
        )
        print(f"Notification response={res}")

        # pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        # print(pubsub_message)
        # print(f"context is {context}")

    except Exception as e:
        e_type, e_value, e_traceback = sys.exc_info()
        logging.error("Exception type : %s " % e_type.__name__)
        logging.error("Exception message : %s " % e_value.__name__)
        logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e
