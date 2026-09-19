import os
import requests


def send_mail(to, subject, body):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox9598d00443e940228c80d7872d0cd008.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY", "API_KEY")),
        data={
            "from": "Mailgun Sandbox <postmaster@sandbox9598d00443e940228c80d7872d0cd008.mailgun.org>",
            "to": to,
            "subject": subject,
            "text": body,
        },
    )
