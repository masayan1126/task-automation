from decimal import ROUND_HALF_UP, Decimal
import math
import os
import requests
from dotenv import load_dotenv
import logging
import sys

import numpy

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

        strategy_param = "mobile"  # モバイルサイト か #PC を指定(mobile or desktop)
        payload = {"strategy": strategy_param, "api_key": os.getenv("GOOGLE_API_KEY")}

        urlName = endpoint + "?url=" + site_url
        # 測定回数
        measurement_count = 3
        scores = []

        for i in range(measurement_count):
            res = requests.get(urlName, params=payload)
            res = res.json()  # jsonに変換

            row_score = res["lighthouseResult"]["categories"]["performance"]["score"]
            score = math.floor(row_score * 100)
            scores.append(score)

        score_average_raw = numpy.average(scores)
        score_average = Decimal(str(score_average_raw)).quantize(
            Decimal("0.1"), rounding=ROUND_HALF_UP
        )
        score_max = numpy.amax(scores)
        score_min = numpy.amin(scores)
        print(f"\n平均 {score_average} 点（最低 {score_min} 点、最高 {score_max} 点）")

    except Exception as e:
        e_type, e_value, e_traceback = sys.exc_info()
        logging.error("Exception type : %s " % e_type.__name__)
        logging.error("Exception message : %s " % e_value.__name__)
        logging.error("Stack trace : %s " % e_traceback.__name__)

        raise e
