from discord_webhook import DiscordWebhook

import os

# DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_notification(webhook_url, message):
    print("알림 전송됨:", webhook_url)  # 로그
    webhook = DiscordWebhook(url=webhook_url, content=message)
    response = webhook.execute()
    print("Response:", response)  # 응답 로그
