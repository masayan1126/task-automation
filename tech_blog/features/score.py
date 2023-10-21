from decimal import ROUND_HALF_UP, Decimal
import math
import time
import requests
import numpy


# 参考：https://zenn.dev/kotahashihama/articles/35133dafa1972bb70df0
def calc_performance_score(payload, urlName, measurement_count):
    scores = []

    for _ in range(measurement_count):
        time.sleep(2)
        res = requests.get(urlName, params=payload)
        data = res.json()

        row_score = data["lighthouseResult"]["categories"]["performance"]["score"]
        score = math.floor(row_score * 100)
        scores.append(score)

    score_average_raw = numpy.average(scores)

    score_average = Decimal(str(score_average_raw)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP
    )
    score_max = numpy.amax(scores)
    score_min = numpy.amin(scores)

    return score_average, score_max, score_min
