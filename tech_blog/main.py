import os
from dotenv import load_dotenv
from features.article import (
    get_article_info_list_from_gcs,
    get_articles_from_mcs,
    update_article_info_list,
)
from taopypy.modules.x import do_tweet
from taopypy.modules.notification import notify_to_slack


# python -c "from tech_blog import main; main.share()"
def share(event=None, context=None):
    try:
        load_dotenv("/Users/masayanishigaki/git/task-automation/tech_blog/.env")

        article_info_list = get_article_info_list_from_gcs()

        # do_tweet(
        #     consumer_key=os.getenv("CONSUMER_KEY", ""),
        #     consumer_secret=os.getenv("CONSUMER_SECRET", ""),
        #     access_token=os.getenv("ACCESS_TOKEN", ""),
        #     access_token_secret=os.getenv("ACCESS_TOKEN_SECRET", ""),
        #     share_content_list=article_info,
        # )

        res = notify_to_slack(
            payload={
                "icon_emoji": ":ghost:",
                "username": "new-bot-name",
                "text": f"定期シェア処理が完了しました\n\n{article_info_list}",
            },
            to=os.getenv("SLACK_WEBHOOK_URL", ""),
        )
        print(f"Notification response={res}")

    except Exception as e:
        print(e)


# python -c "from tech_blog import main; main.collect()"
# 週一でcloud strageからダウンロード
# 新しい生地の差分を追加して再度アップロード
# 下書きは含まれないので注意
def collect(event=None, context=None):
    try:
        load_dotenv("/Users/masayanishigaki/git/task-automation/tech_blog/.env")

        articles = get_articles_from_mcs()

        update_article_info_list(articles)

    except Exception as e:
        # e_type, e_value, e_traceback = sys.exc_info()
        print(e)
        # logging.error("Exception type : %s " % e_type.__name__)
        # logging.error("Exception message : %s " % e_value.__name__)
        # logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e


if __name__ == "__main__":
    share()
