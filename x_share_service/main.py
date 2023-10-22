import json
import tweepy
import os


def share_to_x(request) -> list:
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    share_content_list = __parse(request)

    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )

    for content in share_content_list:
        client.create_tweet(text=f"{content['title']}\n\n{content['url']}")

    return share_content_list


def __parse(req) -> list:
    req_json = req.get_json()
    share_content_list = req_json["share_content_list"]

    return json.loads(share_content_list)
