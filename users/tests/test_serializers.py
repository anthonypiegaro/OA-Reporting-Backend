from django.contrib.auth import get_user_model
from django.test import TestCase
from users.serializers import CustomUserSerializer

class UserEmailValidationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@test.com', password='ahgdhjskfgnHJGjh!')

    def test_valid_user_creation(self):
        serializer = CustomUserSerializer(data={"email": "testUserTwo@test.com", "password": "kjgndfuew7676JHGY!"})
        self.assertTrue(serializer.is_valid())

    def test_invalid_email_should_raise_error(self):
        serializer = CustomUserSerializer(data={"email": "invalid", 'password': 'kjgndfuew7676JHGY!'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_non_uniqie_email_should_raise_error(self):
        serializer = CustomUserSerializer(data={"email": "test@test.com", 'password': 'kjgndfuew7676JHGY!'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_invalid_password_should_raise_error(self):
        serializer = CustomUserSerializer(data={"email": "testUserTwo@test.com", 'password': 'password'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
