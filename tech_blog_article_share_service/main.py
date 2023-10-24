import json
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token
import requests


# 参考：https://zenn.dev/eito_blog/articles/94dc874c112c9f
def main(event=None, context=None):
    load_dotenv()

    article_list = retrieve_blog_article_list()

def retrieve_blog_article_list() -> list:
    tech_blog_article_retrieve_service_endpoint = "https://asia-northeast1-masayan1126.cloudfunctions.net/tech_blog_article_retrieve_service"
    tech_blog_article_retrieve_service_id_token = get_token(
        tech_blog_article_retrieve_service_endpoint
    )

    headers = {
        "Authorization": f"Bearer {tech_blog_article_retrieve_service_id_token}",
        "Content-Type": "application/json",
    }

    res = requests.post(
        url=tech_blog_article_retrieve_service_endpoint,
        headers=headers,
    )

    article_list = json.loads(res.content)

    return article_list

# TODO: これは別のマイクロサービスに共通化する
def get_token(service_endpoint: str) -> str:
    auth_req = Request()
    id_token = fetch_id_token(
        auth_req,
        service_endpoint,
    )

    return id_token