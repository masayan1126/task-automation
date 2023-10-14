import os
from dotenv import load_dotenv
from features.article import (
    get_article_info_list_from_gcs,
    get_articles_from_mcs,
    update_article_info_list,
)
from features.score import calc_performance_score
from taopypy.modules.x import do_tweet
from taopypy.modules.notification import notify_to_slack
from taopypy.modules.formatter.error_formatter import ErrorFormatter


# python -c "from tech_blog import main; main.share()"
def share(event=None, context=None):
    try:
        load_dotenv("/Users/masayanishigaki/git/task-automation/tech_blog/.env")

        article_info_list = get_article_info_list_from_gcs()

        do_tweet(
            consumer_key=os.getenv("CONSUMER_KEY", ""),
            consumer_secret=os.getenv("CONSUMER_SECRET", ""),
            access_token=os.getenv("ACCESS_TOKEN", ""),
            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET", ""),
            share_content_list=article_info_list,
        )

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
        print(e)


# 　TODO：これは、pub subではなく、httpで叩く必要があるかも(vercelでビルドデプロイ完了後に叩く)
def calc_score(event=None, context=None):
    try:
        load_dotenv()

        site_url = "https://maasaablog.com/page/1"
        endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

        strategy_param = "mobile"  # (mobile or desktop)
        payload = {"strategy": strategy_param, "api_key": os.getenv("GOOGLE_API_KEY")}

        urlName = endpoint + "?url=" + site_url
        # 測定回数
        measurement_count = 3

        score_average, score_max, score_min = calc_performance_score(
            payload, urlName, measurement_count
        )
        print(f"\n平均 {score_average} 点（最低 {score_min} 点、最高 {score_max} 点）")

    except Exception as e:
        print(e)
        formatted = ErrorFormatter().format(e)
        print(formatted["message"])
        print(formatted["stack_trace"])


if __name__ == "__main__":
    calc_score()
