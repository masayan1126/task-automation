import os

from dotenv import load_dotenv
import logging
import sys

from features.score import calc_tech_blog_score
from taopypy.modules.formatter.error_formatter import ErrorFormatter

# from notification import notify_to_slack

"""Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """


def main(event, context):
    try:
        load_dotenv()

        site_url = "https://maasaablog.com/page/1"
        endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

        strategy_param = "mobile"  # (mobile or desktop)
        payload = {"strategy": strategy_param, "api_key": os.getenv("GOOGLE_API_KEY")}

        urlName = endpoint + "?url=" + site_url
        # 測定回数
        measurement_count = 1

        score_average, score_max, score_min = calc_tech_blog_score.calc(
            payload, urlName, measurement_count
        )
        print(f"\n平均 {score_average} 点（最低 {score_min} 点、最高 {score_max} 点）")

    except Exception as e:
        formatted = ErrorFormatter().format(e)
        print(formatted["message"])
        print(formatted["stack_trace"])
