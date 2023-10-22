from google.oauth2 import service_account
from google.cloud import storage
import random
import requests
import json
import os


def get_article_info_list_from_gcs():
    """公開済みのブログ記事の情報を取得します(記事の実体を取得するわけではない)

    Returns:
        _type_: _description_
    """
    # client = get_storage_client()
    client = storage.Client()
    bucket = client.get_bucket("tech-blog-articles")
    blob = bucket.blob("data/articles.txt")

    with blob.open("r") as f:
        content = f.read()

        # 形式は以下の通り
        # {
        #     "g60njs1p2xmi": "【GCP】インフラのマイクロサービスをモノレポ構成でCI/CD",
        #     "u2grnxlz9r": "Visual Studio Codeをpython用エディターにするための拡張機能・設定",
        # }
        d = json.loads(content)
        article_ids = list(d.keys())

        BLOG_BASE_PATH = "https://maasaablog.com/blog/"
        NUM_OF_SHARE = 5
        random_article_ids = random.sample(article_ids, NUM_OF_SHARE)
        article_info_list = []
        for article_id in random_article_ids:
            article_info_list.append(
                {
                    "url": BLOG_BASE_PATH + article_id,
                    "title": d[article_id],
                }
            )

    return article_info_list


# def __get_storage_client():
#     scoped_credentials = __get_scoped_credential()
#     client = storage.Client(
#         credentials=scoped_credentials,
#         project=scoped_credentials.project_id,
#     )

#     return client


# def __get_scoped_credential():
#     credentials = service_account.Credentials.from_service_account_file(
#         os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
#     )

#     scoped_credentials = credentials.with_scopes(
#         [
#             "https://www.googleapis.com/auth/cloud-platform",
#         ]
#     )

#     return scoped_credentials


def update_article_info_list(articles) -> None:
    client = storage.Client()
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
