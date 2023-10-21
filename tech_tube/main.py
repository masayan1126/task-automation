import os
from utils import get_random_element_from_list
from services.x.contents_share_to_x_service import do_tweet
from dotenv import load_dotenv
from services.youtube.youtube_video_retrieve_service import (
    retrieve_want_to_share_videos,
)

from taopypy.notification import notify_to_slack


def main(event=None, context=None):
    try:
        load_dotenv()
        # TODO: 処理開始のログを出す

        num_of_retrieve_videos = 2
        want_to_share_videos = retrieve_want_to_share_videos(num_of_retrieve_videos)

        print("チャンネルの動画一覧:")
        for video_info in want_to_share_videos:
            print(f"url: {video_info['url']}, title: {video_info['title']}")

        do_tweet(want_to_share_videos)

        res = notify_to_slack(
            payload={
                "icon_emoji": ":ghost:",
                "username": "new-bot-name",
                "text": f"定期シェア処理が完了しました\n\n{want_to_share_videos}",
            },
            to=os.getenv("SLACK_WEBHOOK_URL"),
        )
        print(f"Notification response={res}")

        # pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        # print(pubsub_message)
        # print(f"context is {context}")

    except Exception as e:
        print(e)
