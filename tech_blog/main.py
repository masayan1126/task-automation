import os
import random
from dotenv import load_dotenv
from taopypy.modules.x import do_tweet
from taopypy.modules.notification import notify_to_slack
import requests
from google.cloud import storage
from google.oauth2 import service_account
import json


# python -c "from tech_blog import main; main.share()"
def share(event=None, context=None):
    try:
        load_dotenv("/Users/masayanishigaki/git/task-automation/tech_blog/.env")

        # service_account.Credentials
        # credentials = service_account.Credentials.from_service_account_file(
        #     os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
        # )

        # scoped_credentials = credentials.with_scopes(
        #     [
        #         "https://www.googleapis.com/auth/cloud-platform",
        #     ]
        # )

        client = storage.Client(
            # credentials=scoped_credentials,
            # project=scoped_credentials.project_id,
        )

        bucket = client.get_bucket("tech-blog-articles")

        blob = bucket.blob("data/articles.txt")

        with blob.open("r") as f:
            content = f.read()

            # 形式は以下の通り
            # {
            #     "g60njs1p2xmi": "【GCP】インフラのマイクロサービスをモノレポ構成でCI/CD",
            #     "u2grnxlz9r": "Visual Studio Codeをpython用エディターにするための拡張機能・設定",
            #     "9ti_85iu0t": "Dockerコマンド1発でDockerfile、compose.yml、.dockerignoreを自動生成する",
            #     "itpmmty931kd": "【ChatGpt】CodeRabbitとGithubActionsを連携してプルリクエストのレビューと要約を自動生成する",
            # }
            d = json.loads(content)
            article_ids = list(d.keys())

            BLOG_BASE_PATH = "https://maasaablog.com/blog/"
            NUM_OF_SHARE = 5
            random_article_ids = random.sample(article_ids, NUM_OF_SHARE)
            articles = []
            for article_id in random_article_ids:
                articles.append(
                    {
                        "url": BLOG_BASE_PATH + article_id,
                        "title": d[article_id],
                    }
                )

        # do_tweet(
        #     consumer_key=os.getenv("CONSUMER_KEY", ""),
        #     consumer_secret=os.getenv("CONSUMER_SECRET", ""),
        #     access_token=os.getenv("ACCESS_TOKEN", ""),
        #     access_token_secret=os.getenv("ACCESS_TOKEN_SECRET", ""),
        #     share_content_list=articles,
        # )

        res = notify_to_slack(
            payload={
                "icon_emoji": ":ghost:",
                "username": "new-bot-name",
                "text": f"定期シェア処理が完了しました\n\n{articles}",
            },
            to=os.getenv("SLACK_WEBHOOK_URL", ""),
        )
        print(f"Notification response={res}")

    except Exception as e:
        # e_type, e_value, e_traceback = sys.exc_info()
        print(e)
        # logging.error("Exception type : %s " % e_type.__name__)
        # logging.error("Exception message : %s " % e_value.__name__)
        # logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e


# python -c "from tech_blog import main; main.collect()"
# 週一でcloud strageからダウンロード
# 新しい生地の差分を追加して再度アップロード
# 下書きは含まれないので注意
def collect(event=None, context=None):
    try:
        load_dotenv("/Users/masayanishigaki/git/task-automation/tech_blog/.env")

        articles = []

        ENDPOINT = "https://quxwm5ub3d.microcms.io/api/v1/blogs?limit=100&offset=320"

        X_MICROCMS_API_KEY = os.getenv("X_MICROCMS_API_KEY", "")

        headers = {"X-MICROCMS-API-KEY": X_MICROCMS_API_KEY}

        res = requests.get(ENDPOINT, headers=headers)
        data = res.json()

        for article in data["contents"]:
            articles.append(
                {
                    "id": article["id"],
                    "title": article["title"],
                }
            )

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

        blob = bucket.blob("data/articles.txt")

        with blob.open("r") as f:
            content = f.read()
            if content == "":
                d = {}
            else:
                d = json.loads(content)

            for article in articles:
                article_id = article["id"]
                if article_id not in d:
                    d[article_id] = article["title"]

            blob.upload_from_string(json.dumps(d))

    except Exception as e:
        # e_type, e_value, e_traceback = sys.exc_info()
        print(e)
        # logging.error("Exception type : %s " % e_type.__name__)
        # logging.error("Exception message : %s " % e_value.__name__)
        # logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e
