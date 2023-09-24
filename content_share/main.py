import tweepy
from dotenv import load_dotenv
import os
import base64

"""Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """


def main(event, context):
    load_dotenv()
    # TODO: cloud schedulerからシェアするコンテンツの情報をjsonなどで受け取る
    __do_tweet()

    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    print(pubsub_message)
    return "Hello {}!!Q".format("name")


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
        text="【Genie AI】VSCodeにインストールすべきChatGPT拡張\n\nhttps://www.youtube.com/watch?v=ngLbfn_3KfQ&feature=youtu.be"
    )
