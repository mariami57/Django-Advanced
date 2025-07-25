from unittest.mock import patch

from django.test import TestCase

from posts.tasks import _send_mail


class TestSendEmailTask(TestCase):

    @patch('posts.tasks.send_mail')
    async def test__send_mail__calls_django_send_mail_func(self, mock_django_send_mail):
        await _send_mail(
            subject="Test subject",
            message="Test message",
            from_email="test@test.com",
            recipient_list=['test@test.com'],
        )

        mock_django_send_mail.assert_called_with(
            subject="Test subject",
            message="Test message",
            from_email="test@test.com",
            recipient_list=['test@test.com'],
        )

