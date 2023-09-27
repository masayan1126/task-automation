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

        __my_movies()
        __notify_to_slack()
        return "Hello {}!!Q".format("name")

        # pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        # print(pubsub_message)
        # print(f"context is {context}")

    except Exception as e:
        print(f"Exception is {e}")
        raise e


def __notify_to_slack():
    payload = {
        "icon_emoji": ":ghost:",
        "username": "new-bot-name",
        "text": "定期実行処理が完了しました",
    }

    headers = {"Content-Type": "application/json; charset=UTF-8"}
    res = requests.post(
        url=os.getenv("SLACK_WEBHOOK_URL"),
        headers=headers,
        data=json.dumps(payload),
        proxies=None,
    )
    print(res)


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


def __my_movies():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    API_VER = "v3"
    youtube = build("youtube", API_VER, developerKey=GOOGLE_API_KEY)
    channel_id = "UC5AcEeC1LjJ7f5-o5jxfzqQ"

    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,  # 1回のリクエストで取得する最大動画数
            pageToken=next_page_token,
        )

        response = request.execute()
        print(response["items"])

        for item in response["items"]:
            if item["id"]["kind"] is "youtube#video":
                video_id = item["id"]["videoId"]
                videos.append(video_id)

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    print("チャンネルの動画一覧:")
    for video_id in videos:
        print(f"https://www.youtube.com/watch?v={video_id}")


# if __name__ == "__main__":
#     main()


# [
#     {
#         "kind": "youtube#searchResult",
#         "etag": "EOrmAypDjnVdvPLSUlNoAEd554E",
#         "id": {
#             "kind": "youtube#playlist",
#             "playlistId": "PL2VK2ZJib1yT659MkMS60pOrMcontPnRE",
#         },
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "0y6123BQ-cuUqrUb5QOjjECbaTc",
#         "id": {
#             "kind": "youtube#playlist",
#             "playlistId": "PL2VK2ZJib1yQGI9XYyWulZ8kTLmSoBFqt",
#         },
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "hj7p-Hwkj4HzXKHERRpU1q56t2o",
#         "id": {"kind": "youtube#video", "videoId": "7FTjlE7FYZ8"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "9VAHRAGVk8G2GxUr7CSEtkym7tc",
#         "id": {"kind": "youtube#channel", "channelId": "UC5AcEeC1LjJ7f5-o5jxfzqQ"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "v6OL1OlIq1QEGz9M1B1fm0QeM5o",
#         "id": {"kind": "youtube#video", "videoId": "a9UJ99caBTQ"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "PDPo0NSBzE2varAEb3C869CmY0I",
#         "id": {"kind": "youtube#video", "videoId": "c9hQhKth8iU"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "CRigvJMlKPmqy3umUmcjrGZOJAs",
#         "id": {"kind": "youtube#video", "videoId": "Z2Dn6Xtqb6I"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "pyGmYBEBfj_wveG_kWq45KC_Js8",
#         "id": {"kind": "youtube#video", "videoId": "Kn79ySfhjU4"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "mYsGNL1zovu7eti0FFZiIrx854c",
#         "id": {"kind": "youtube#video", "videoId": "7jYfbwp5-RE"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "hT4xKCA3wAX2u8PnUkZcnexlOks",
#         "id": {"kind": "youtube#video", "videoId": "3gWDy9RvO3o"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "yxOqQznplS2CzHF7_H9NphssMhw",
#         "id": {"kind": "youtube#video", "videoId": "ngLbfn_3KfQ"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "XJYr0cBjiseEACCizu_h_THnuxg",
#         "id": {"kind": "youtube#video", "videoId": "Y0mi-TeifGw"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "Z8bMkiZDjX-V0fnn4jh2GP7oZYM",
#         "id": {"kind": "youtube#video", "videoId": "XFHRqDm8mGY"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "RmznpHmGQdtjpN6E6rE_EO8dvvU",
#         "id": {"kind": "youtube#video", "videoId": "xiPaKX_jXfo"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "4B1a1Y7VyJIC9nnIJZtxJRJGRd0",
#         "id": {"kind": "youtube#video", "videoId": "V9qjLwNRok0"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "b2nno5qV6pzRoxPeRyBM6WQXeKg",
#         "id": {"kind": "youtube#video", "videoId": "_hgBdyUdsJY"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "YSDYzmNNZubKEJHLAc8HAskfzy0",
#         "id": {"kind": "youtube#video", "videoId": "xHTfurcPnQI"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "D9kMU-uNZ1liMxmbL3zWcovdz4w",
#         "id": {"kind": "youtube#video", "videoId": "bHzosAFR9E8"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "0U4JWfJMOOkQxNYYDlP25cEULiE",
#         "id": {"kind": "youtube#video", "videoId": "nciZU1Aedgw"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "rxFGy2r-v25sXntGZG_-jeud540",
#         "id": {"kind": "youtube#video", "videoId": "hxCvKdFBH9s"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "JWI8zfLBVdtzCp80gGxD3d6PBsA",
#         "id": {"kind": "youtube#video", "videoId": "0E5isjlv_KQ"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "8cmDM4q3BevY-IUsFKCph8vzELs",
#         "id": {"kind": "youtube#video", "videoId": "nLg0bV8sfbw"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "x8ppR04geiWtwVuVfnLJe0reLdU",
#         "id": {"kind": "youtube#video", "videoId": "0VCsNnZhh5A"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "8qxicSqdYP-FicwtA_uugXrkUqY",
#         "id": {"kind": "youtube#video", "videoId": "KxV7HUoKves"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "_DRz9D44kQSrvT5hk3dv3VlXXDA",
#         "id": {"kind": "youtube#video", "videoId": "S_3SYW18JvE"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "xyuwQli7JLM5fEgL0wyg8g6OuKM",
#         "id": {"kind": "youtube#video", "videoId": "D27_INiAaxA"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "YhaNkSAULLGqvKDHtfy4UOCnxN8",
#         "id": {"kind": "youtube#video", "videoId": "RGLUq-dB7sI"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "c22vHnHIh_-AULoTHHrWBAV2Pg0",
#         "id": {"kind": "youtube#video", "videoId": "o7_qitgem2w"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "hgWqBaswpqKdRGXOmF8Xqry6Cqc",
#         "id": {"kind": "youtube#video", "videoId": "zDHWLUTwXZQ"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "7hz7ca23sNyumweytBPNNO2sFzA",
#         "id": {"kind": "youtube#video", "videoId": "meIcSZI-rVI"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "51X68Vk23H0-P7612NJkq12CXXU",
#         "id": {"kind": "youtube#video", "videoId": "q-LdsnYdYmc"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "ad3lLVD8pRfnsv9mVFugOskAMtA",
#         "id": {"kind": "youtube#video", "videoId": "xZfP98BKcN4"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "9ONK226kjc6xt7T7f-1-C4fATyw",
#         "id": {"kind": "youtube#video", "videoId": "_ULY3S4-KVs"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "4Y_hOuIN-ny232OnlTuWtL5wQaY",
#         "id": {"kind": "youtube#video", "videoId": "IOZd6pp_pc4"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "bTOZcNHHjC0MMql0D8xTavWlkJw",
#         "id": {"kind": "youtube#video", "videoId": "2Yy-pWnQvdE"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "ghcyX90z4GaWvT46G7RrjYj-l8U",
#         "id": {"kind": "youtube#video", "videoId": "40GWEutdMpg"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "xSR3rNeo0oxt4vb1kgHaBByCgZA",
#         "id": {"kind": "youtube#video", "videoId": "_f8uVT-71Jo"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "8DET4K-WugMgaLyPjGgPgVbf5dE",
#         "id": {"kind": "youtube#video", "videoId": "1GyUap13cyM"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "Iq3X4GWBi9Tqpa3gj9CAJfrvU-0",
#         "id": {"kind": "youtube#video", "videoId": "mMwgOtXGSp0"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "-d1mPrB5hFwb3_hrv_d6iBrPiGE",
#         "id": {"kind": "youtube#video", "videoId": "G8aNfZ0sGKU"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "pxQFMOye_W3c4_g4naFhxJSr4M8",
#         "id": {"kind": "youtube#video", "videoId": "ruvrsb4f26I"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "hsQ4tZyEM5Rr4AaeQFgJv8vpO2c",
#         "id": {"kind": "youtube#video", "videoId": "PLKjlYnhW8M"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "NINGrH6qabcBTwwTl2mx7iBbMDY",
#         "id": {"kind": "youtube#video", "videoId": "ZHnzxDS44DE"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "j1ZmRRFdB9z-ZcFd5eTJb1Uu9JI",
#         "id": {"kind": "youtube#video", "videoId": "auifMrk5kBQ"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "IYpVSsuY4zcfx-CLFwRLorq3vFs",
#         "id": {"kind": "youtube#video", "videoId": "aes77Iei_GI"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "0jfsLJVif7CuznchKFM4L0dZDPs",
#         "id": {"kind": "youtube#video", "videoId": "AqdoPlhbwhw"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "5M6299Bsb_DrmDAffA6BhiUvxv4",
#         "id": {"kind": "youtube#video", "videoId": "fj-OU65Ywh4"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "055dn86ntM5brHyEnLbADwR3i3U",
#         "id": {"kind": "youtube#video", "videoId": "efrC0hN9zlY"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "9k5zisdfnUzLCFEXmz_LCcX_2aY",
#         "id": {"kind": "youtube#video", "videoId": "-9ul7gUH9qI"},
#     },
#     {
#         "kind": "youtube#searchResult",
#         "etag": "Naco6XbFzn-Tm6otmCDXIGLmkw0",
#         "id": {"kind": "youtube#video", "videoId": "cJT9rYNnMmo"},
#     },
# ]
