from decimal import ROUND_HALF_UP, Decimal
import math
import time
import requests
import numpy


def calc(payload, urlName, measurement_count):
    scores = []

    for _ in range(measurement_count):
        time.sleep(5)
        res = requests.get(urlName, params=payload)
    #     res = res.json()

    #     row_score = res["lighthouseResult"]["categories"]["performance"]["score"]
    #     score = math.floor(row_score * 100)
    #     scores.append(score)

    # score_average_raw = numpy.average(scores)

    # score_average = Decimal(str(score_average_raw)).quantize(
    #     Decimal("0.1"), rounding=ROUND_HALF_UP
    # )
    # score_max = numpy.amax(scores)
    # score_min = numpy.amin(scores)

    # return score_average, score_max, score_min
    return 1, 1, 1
