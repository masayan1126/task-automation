import json
import random
from google.cloud import storage


def retrieve_blog_articles(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    article_info_list = get_article_info_list_from_gcs()

    return json.dumps(article_info_list)


def get_article_info_list_from_gcs():
    """公開済みのブログ記事の情報を取得します(記事の実体を取得するわけではない)

    Returns:
        _type_: _description_
    """
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
