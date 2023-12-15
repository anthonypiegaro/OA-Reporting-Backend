import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import CustomUser 

import ssl
ssl._create_default_https_context = ssl._create_unverified_context



@receiver(post_save, sender=CustomUser)
def send_confirmation_email(sender, instance, created, **kwargs):
    """
    Custom signal handler to send a confirmation email to newly registered users.
    """
    if created:  # Only send the email if the user was just created
        name = instance.first_name + " " + instance.last_name
        html_content = render_to_string('intro_email.html', {'name': name})
        plain_text_content = strip_tags(html_content)
        subject = "Welcome to Optimum Athletes - Your Journey to Peak Performance Begins!"
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=instance.email,
            subject=subject,
            html_content=html_content,
            plain_text_content=plain_text_content,
        )
        print(settings.DEFAULT_FROM_EMAIL)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(instance.email)
        print("success")
        return response.status_code
    except Exception as e:
        print("fail")
        print(e)
        return str(e)
