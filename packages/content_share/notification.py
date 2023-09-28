import requests
import json
import os


def notify_to_slack(payload: dict) -> requests.Response:
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    res = requests.post(
        url=os.getenv("SLACK_WEBHOOK_URL"),
        headers=headers,
        data=json.dumps(payload),
        proxies=None,
    )

    return res
