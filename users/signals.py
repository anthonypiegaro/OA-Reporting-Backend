import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
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
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=instance.email,
            subject="Welcome to Optimum Athletes Reporting",
            plain_text_content="Your Optimum Athletes Data Dashboard has been created.\n\n" + \
            f'Go to optimumathletesreporting.com \n\n' + \
            f'To sign in, use {instance.email} for the email.\n' + \
            "Your password is Baseball + Initials + @. For example:\n" + \
            "Athlete Name: John Doe - Password: Baseballjd@"
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
