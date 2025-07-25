from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posts.models import Post

UserModel = get_user_model()
class TestApprovePostView(TestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'test',
            'email': 'test@test.com',
            'password': '12mimi34',
        }

        self.user = UserModel.objects.create_user(
            **self.user_credentials
        )

        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user,
            approved=False,
        )

        self.client.login(
            email=self.user_credentials['email'],
            password=self.user_credentials['password']
        )

    def test__approve_valid_post__approves_the_post_and_redirects(self):
        response = self.client.post(
            reverse('approve_post', args=[self.post.pk]),
            HTTP_REFERER = reverse('dashboard')
        )

        self.post.refresh_from_db()

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(self.post.approved)

    def test__invalid_post__raises_DoesNotExistError(self):
        with self.assertRaises(self.post.DoesNotExist) as dne:
            self.client.post(
                reverse('approve_post', args=[999]),
                HTTP_REFERER=reverse('dashboard')
            )

        self.assertTrue(str(dne))
