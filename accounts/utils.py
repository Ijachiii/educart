from django.core.mail import send_mail
from django.template.loader import render_to_string
import jwt
from educart_project.settings import SECRET_KEY
from datetime import datetime
from django.utils import timezone

def send_otp_signup(email, first_name, otp):
    context = {"otp": otp, "first_name": first_name}
    html_content = render_to_string("signup_email_otp.html", context)

    send_mail(
        "VERIFICATION OTP",
        f"Enter the 4-digit code below to verify your identity \n\n{otp}",
        "info@hackcity.tech",
        [email],
        fail_silently=False,
        html_message=html_content
    )

def send_otp_login(email, first_name, otp):
    context = {"otp": otp, "first_name": first_name}
    html_content = render_to_string("login_email_otp.html", context)

    send_mail(
        "VERIFICATION OTP",
        f"Enter the 4-digit code below to verify your identity \n\n{otp}",
        "info@hackcity.tech",
        [email],
        fail_silently=False,
        html_message=html_content
    )

def send_otp_password_reset(email, first_name, otp):
    context = {"otp": otp, "first_name": first_name}
    html_content = render_to_string("password_reset_email_otp.html", context)

    send_mail(
        "VERIFICATION OTP",
        f"Enter the 4-digit code below to verify your identity \n\n{otp}",
        "info@hackcity.tech",
        [email],
        fail_silently=False,
        html_message=html_content
    )

def send_otp_pin_reset(email, first_name, otp):
    context = {"otp": otp, "first_name": first_name}
    html_content = render_to_string("pin_reset_email_otp.html", context)

    send_mail(
        "VERIFICATION OTP",
        f"Enter the 4-digit code below to verify your identity \n\n{otp}",
        "info@hackcity.tech",
        [email],
        fail_silently=False,
        html_message=html_content
    )


def get_token_expiry_time(access_token):
    encoded_token = access_token
    decoded_token = jwt.decode(encoded_token, SECRET_KEY, algorithms=["HS256"])
    expiration_timestamp = decoded_token['exp']
    return expiration_timestamp

