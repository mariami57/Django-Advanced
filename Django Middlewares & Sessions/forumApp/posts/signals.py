from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from posts.models import Post
from posts.tasks import _send_mail


@receiver(signal=post_save, sender=Post)
def send_approval_email_notification(sender, instance, created, **kwargs):
    if not created and instance.approved:
        _send_mail.delay(
            subject='Your post has been approved',
            message=f'Hi {instance.author.username},\n\n Your post has been approved.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.author.email]
        )