import base64
import ssl
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL
from typing import Any, Union

import jwt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import HTTPException
from passlib.context import CryptContext

from common import templates_env
from config import settings
from utils import cryptography

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def create_verify_email_link(email: str) -> str:
    code = cryptography.encrypt_json({'user_email': email}, settings.EMAIL_VERIFY_KEY)
    return f'{settings.FRONTEND_URL}/email-verify/{code}'


def verify_email(email: str):
    template = templates_env.get_template('verify_email.html')
    body = template.render({'verify_link': create_verify_email_link(email)})
    msg = MIMEText(body, 'html')
    msg['Subject'] = 'Verify Your Email'
    msg['From'] = 'from@events.com'
    msg['To'] = email
    # Connect to the email server
    try:
        server = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls(context=ssl.create_default_context())  # Secure the connection
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)  # Send the email
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
