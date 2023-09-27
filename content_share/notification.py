import requests
import json
import os


def notify_to_slack() -> requests.Response:
    payload = {
        "icon_emoji": ":ghost:",
        "username": "new-bot-name",
        "text": "定期実行処理が完了しました",
    }

    headers = {"Content-Type": "application/json; charset=UTF-8"}
    res = requests.post(
        url=os.getenv("SLACK_WEBHOOK_URL"),
        headers=headers,
        data=json.dumps(payload),
        proxies=None,
    )

    return res
