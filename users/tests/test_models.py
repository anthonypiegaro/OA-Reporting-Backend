from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase


# Create your tests here.
class UserCreationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="testUser@test.com", password="1jy3bHJGBYUGk687b!")

    def test_user_creation(self):
        userTwo = get_user_model().objects.create_user(email="testUserTwo@test.com", password="1jy3bHJGBYUGk687b!")
        self.assertEqual(userTwo.email, "testUserTwo@test.com")
    
    def test_invalid_email_should_raise_error(self):
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(email="invalid", password="1jy3bHJGBYUGk687b!")

    def test_non_unique_email_should_raise_error(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(email="testUser@test.com", password="1jy3bHJGBYUGk687b!")
    
    def test_invalid_password_should_raise_error(self):
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(email="testUserTwo@test.com", password="password")
