import os

from dotenv import load_dotenv
import logging
import sys

from features.score import calc_tech_blog_score


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
        measurement_count = 3

        score_average, score_max, score_min = calc_tech_blog_score.calc(
            payload, urlName, measurement_count
        )
        print(f"\n平均 {score_average} 点（最低 {score_min} 点、最高 {score_max} 点）")

    except Exception as e:
        e_type, e_value, e_traceback = sys.exc_info()
        logging.error("Exception type : %s " % e_type.__name__)
        logging.error("Exception message : %s " % e_value.__name__)
        logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e
