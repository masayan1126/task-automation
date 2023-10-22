import base64
import json
import os
from dotenv import load_dotenv
from google.cloud import pubsub_v1
import requests


# 参考：https://zenn.dev/eito_blog/articles/94dc874c112c9f
def main(event=None, context=None):
    load_dotenv()

    data = {
        "google_api_key": "AIzaSyDujSCmj2xcx_620BeN2aSX140XmcP-5A0",
        "channel_id": "UC5AcEeC1LjJ7f5-o5jxfzqQ",
    }

    res = requests.post(
        "https://asia-northeast1-masayan1126.cloudfunctions.net/youtube_video_retrieve_service",
        data=data,
    )

    print(res.content, flush=True)

    # destination_topic = base64.b64decode(event["data"]).decode("utf-8")
    # print(destination_topic)

    # publisher = pubsub_v1.PublisherClient()
    # topic_path = publisher.topic_path(
    #     os.environ.get("GCP_PROJECT_ID", ""), topic="youtube_video_retrieve_service"
    # )

    # data = {
    #     "share": {"topic_id": "x_share_service"},
    #     "notification": {
    #         "topic_id": "youtube_video_retrieve_service",
    #         "slack_web_hoook": "youtube_video_retrieve_service",
    #     },
    # }

    # data_str = "x_share_service"
    # Data must be a bytestring
    # data = json.dumps(data).encode("utf-8")

    # future = publisher.publish(topic_path, data)
