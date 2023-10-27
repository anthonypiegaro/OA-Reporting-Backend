from django.contrib.auth import get_user_model
from django.urls import reverse
from http.cookies import SimpleCookie
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.serializers import CustomUserSerializer

class CustomUserViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.com', password='kjhdfJHJHjhflnkjwh876!')
        self.client.force_authenticate(user=self.user)

        self.superuser_client = APIClient()
        self.superuser = get_user_model().objects.create_user(email='superuser@example.com', password='kjhdfJHJHjhflnkjwh876!', is_staff=True)
        self.superuser_client.force_authenticate(user=self.superuser)


    def test_list_users_returns_ok_and_non_empty_list(self):
        response = self.superuser_client.get(reverse('customuser-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_non_superuser_list_user_returns_forbidden(self):
        response = self.client.get(reverse('customuser-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_returns_ok_and_matching_data(self):
        response = self.client.get(reverse('customuser-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CustomUserSerializer(self.user).data)

    def test_create_user_returns_created_and_user_exists(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'jhGFTYjhgbTF!'
        }
        response = self.superuser_client.post(reverse('customuser-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(email='newuser@example.com').exists())
    
    def test_create_user_invalid_email_returns_bad_request(self):
        data = {
            "email": "invalid",
            "password": "jhGFTYjhgbTF!",
        }
        response = self.superuser_client.post(reverse("customuser-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_non_unique_email_returns_bad_request(self):
        data = {
            "email": "test@example.com",
            "password": "jhGFTYjhgbTF!"
        }
        response = self.superuser_client.post(reverse("customuser-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTestCase(APITestCase):

    def test_logout_ok(self):
        client = APIClient()
        url = reverse("logout")
        response = client.post(url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
