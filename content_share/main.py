import tweepy
from dotenv import load_dotenv
import os
import functions_framework
import base64


@functions_framework.http
def main(event, context):
    load_dotenv()

    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )

    client.create_tweet(text="テストツイート文a")

    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    print(pubsub_message)
    return "Hello {}!!Q".format("name")
