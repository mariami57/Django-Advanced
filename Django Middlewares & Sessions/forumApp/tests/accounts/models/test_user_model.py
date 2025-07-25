from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class TestUserModel(TestCase):
    def setUp(self):
        self.username = "TestUsername"
        self.email = "test@test.com"
        self.password = "12test34"

        self.user = UserModel.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )


    def test__valid_str_method__returns_username(self):

        self.assertEqual(self.username, str(self.user))

    def test__second_user_with_same_username__raise_integrity_error(self):
        with self.assertRaises(IntegrityError) as ie:

            UserModel.objects.create_user(
                username=self.username,
                email="a" + self.email,
                password=self.password
            )

        self.assertIsInstance(ie.exception, IntegrityError)

