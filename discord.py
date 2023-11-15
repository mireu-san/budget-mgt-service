from discordwebhook import Discord


# discord = Discord(url="<web hook url>")
# discord.post(content="Hello, world.")


def send_discord_notification(webhook_url, message):
    webhook = DiscordWebhook(url=webhook_url, content=message)
    response = webhook.execute()
