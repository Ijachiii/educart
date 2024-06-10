from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_congratulatory_consultation(email, name, order_id, amount):
    context = { "name": name, "order_id": order_id, "amount": amount}
    html_content = render_to_string("congratulatory_email_consultation.html", context)

    send_mail(
        "Confirmation of Consultation Submission and Payment Instructions",
        f"",
        "info@hackcity.tech",
        [email],
        fail_silently=False,
        html_message=html_content
    )