import ssl
from email.mime.text import MIMEText
from smtplib import SMTP

from fastapi import HTTPException

from common import templates_env
from config import settings
from utils import cryptography


def create_verify_email_link(email: str) -> str:
    code = cryptography.encrypt_json({'user_email': email}, settings.EMAIL_VERIFY_KEY)
    return f'{settings.FRONTEND_URL}/email-verify/{code}'


def make_reset_password_link(email: str) -> str:
    code = cryptography.encrypt_json({'user_email': email}, settings.RESET_PASSWORD_KEY)
    return f'{settings.FRONTEND_URL}/reset-password/{code}'


def verify_email(email: str) -> None:
    template = templates_env.get_template('verify_email.html')
    send_email('Verify Your Email', template.render({'link': create_verify_email_link(email)}), email)


def reset_password(email: str) -> None:
    template = templates_env.get_template('reset_password.html')
    send_email('Reset password', template.render({'link': make_reset_password_link(email)}), email)


def google_success_oauth(email: str, password: str) -> None:
    template = templates_env.get_template('success_google_oauth.html')
    send_email(
        'You success auth via Google',
        template.render({
            'email': email,
            'password': password,
            'link': f'{settings.FRONTEND_URL}/signin'
        }),
        email
    )


def send_email(subject: str, body: str, to_email: str) -> None:
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = 'from@events.com'
    msg['To'] = to_email
    # Connect to the email server
    try:
        server = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls(context=ssl.create_default_context())  # Secure the connection
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)  # Send the email
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
