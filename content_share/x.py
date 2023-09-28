import tweepy
import os


def do_tweet(share_content_list: list) -> list:
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )

    for content in share_content_list:
        client.create_tweet(text=f"{content['title']}\n\n{content['url']}")

    return share_content_list
