import os
from dotenv import load_dotenv
import jinja2
import requests

load_dotenv()

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)


def send_mail(to, subject, body, html):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox9598d00443e940228c80d7872d0cd008.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY", "API_KEY")),
        data={
            "from": "Flask Store <postmaster@sandbox9598d00443e940228c80d7872d0cd008.mailgun.org>",
            "to": to,
            "subject": subject,
            "text": body,
            "html": html,
        },
    )


def send_user_registration_email(email, username):
    return send_mail(
        email,
        "Successfully Signup.",
        f"Hi {username} You Have Successfully SignUp to the stores rest api.",
        render_template("email/action.html", username=username),
    )
