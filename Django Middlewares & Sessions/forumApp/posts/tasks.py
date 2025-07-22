import asyncio

from asgiref.sync import sync_to_async
from celery import shared_task
from django.core.mail import send_mail
import time

@shared_task
async def _send_mail(subject, message, from_email, recipient_list):
    await asyncio.sleep(5)
    await sync_to_async(send_mail)(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list
    )
