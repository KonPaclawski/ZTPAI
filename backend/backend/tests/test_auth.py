from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from backend.backend.models import User
import json

class AuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.refresh_url = reverse('token_refresh')

        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password=make_password("password123"),
            role="user"
        )

    def test_login_success(self):
        data = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json())
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)

    def test_login_fail_wrong_password(self):
        data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get('error'), "Invalid credentials")

    def test_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), "Logged out")
        self.assertTrue('access_token' in response.cookies)
        self.assertTrue('refresh_token' in response.cookies)

    def test_token_refresh_success(self):
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        login_response = self.client.post(self.login_url, data=json.dumps(login_data), content_type='application/json')
        refresh_token = login_response.cookies.get('refresh_token').value

        self.client.cookies['refresh_token'] = refresh_token
        refresh_response = self.client.post(self.refresh_url)
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn('access', refresh_response.json())
        self.assertIn('access_token', refresh_response.cookies)

    def test_token_refresh_fail_no_token(self):
        response = self.client.post(self.refresh_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get('error'), "No refresh token provided")
