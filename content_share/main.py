import tweepy
from dotenv import load_dotenv
import os
import base64
from apiclient.discovery import build
import slackweb

"""Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """


# TODO: GCP Pub / Sub エミュレータ
def main(event, context):
    try:
        load_dotenv()
        # TODO: cloud schedulerからシェアするコンテンツの情報をjsonなどで受け取る
        __do_tweet()

        __my_movies()

        pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        print(pubsub_message)

        slack = slackweb.Slack(
            url="https://hooks.slack.com/services/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"
        )
        slack.notify(text=f"{context}。デプロイが完了しました")
        return "Hello {}!!Q".format("name")
    except Exception as e:
        print(e)


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
    item = channel["items"]["contentDetails"]
    print(f"My channel is ={item}")
