import os
from dotenv import load_dotenv
from taopypy.modules.x import do_tweet
from taopypy.modules.notification import notify_to_slack
import requests
from google.cloud import storage
from google.oauth2 import service_account
import pandas as pd


def share(event, context):
    try:
        load_dotenv()

        articles = [
            {
                "url": "https://maasaablog.com/blog/g60njs1p2xmi/",
                "title": "【GCP】インフラのマイクロサービスをモノレポ構成でCI/CD",
            },
            {
                "url": "https://maasaablog.com/blog/9ti_85iu0t/",
                "title": "Dockerコマンド1発でDockerfile、compose.yml、.dockerignoreを自動生成する",
            },
            {
                "url": "https://maasaablog.com/blog/4fkllh-xgs14/",
                "title": "【サーバーレス 第一世代Cloud FunctionsをCloud Schedulerで定期実行】Part2：Cloud Schedulerでスケジュール設定・CI/CDパイプライン構築",
            },
        ]

        print("対象の記事一覧:")
        for article in articles:
            print(f"url: {article['url']}, title: {article['title']}")

        # share_content_list = get_random_element_from_list(articles, 2)

        do_tweet(
            consumer_key=os.getenv("CONSUMER_KEY", ""),
            consumer_secret=os.getenv("CONSUMER_SECRET", ""),
            access_token=os.getenv("ACCESS_TOKEN", ""),
            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET", ""),
            share_content_list=articles,
        )

        res = notify_to_slack(
            payload={
                "icon_emoji": ":ghost:",
                "username": "new-bot-name",
                "text": f"定期シェア処理が完了しました\n\n{articles}",
            },
            to=os.getenv("SLACK_WEBHOOK_URL", ""),
        )
        print(f"Notification response={res}")

        # pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        # print(pubsub_message)
        # print(f"context is {context}")

    except Exception as e:
        # e_type, e_value, e_traceback = sys.exc_info()
        print(e)
        # logging.error("Exception type : %s " % e_type.__name__)
        # logging.error("Exception message : %s " % e_value.__name__)
        # logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e


def collect(event, context):
    try:
        load_dotenv()

        # articles = []

        # ENDPOINT = "https://quxwm5ub3d.microcms.io/api/v1/blogs?limit=10&offset=0"

        # X_MICROCMS_API_KEY = os.getenv("X_MICROCMS_API_KEY", "")

        # headers = {"X-MICROCMS-API-KEY": X_MICROCMS_API_KEY}

        # res = requests.get(ENDPOINT, headers=headers)
        # data = res.json()

        # for article in data["contents"]:
        #     articles.append(
        #         {
        #             "id": article["id"],
        #             "title": article["title"],
        #         }
        #     )

        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
        )

        scoped_credentials = credentials.with_scopes(
            [
                "https://www.googleapis.com/auth/cloud-platform",
            ]
        )

        client = storage.Client(
            credentials=scoped_credentials,
            project=scoped_credentials.project_id,
        )

        bucket = client.get_bucket("tech-blog-articles")

        # 格納するGCSパスを指定
        blob = bucket.blob("data/articles.txt")  # アップロード後のファイル名

        df = pd.DataFrame([[1, 2, 3], [5, 6, 7]], columns=["x", "y", "z"])
        # DataFrameをGCSにUpload(ヘッダーは入れるが、インデックスは落とす)
        blob.upload_from_string(df.to_csv(sep=","))

        # 週一で
        # cloud strageからダウンロード
        # idの配列を取得し、配列の中にないIDを元の配列に追加して再度アップロード

        # print("対象の記事一覧:")
        # for article in articles:
        #     print(f"id: {article['id']}, title: {article['title']}")

    except Exception as e:
        # e_type, e_value, e_traceback = sys.exc_info()
        print(e)
        # logging.error("Exception type : %s " % e_type.__name__)
        # logging.error("Exception message : %s " % e_value.__name__)
        # logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e
