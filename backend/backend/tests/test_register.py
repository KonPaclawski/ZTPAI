from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from backend.backend.models import User
from django.contrib.auth.hashers import check_password

class UserAPITestCase(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(name="admin", email="admin@admin.com", password="adminpass", role="admin")
        self.user = User.objects.create_user(name="user1", email="user1@example.com", password="userpass", role="user")
        self.client = APIClient()

    def test_register_user_success(self):
        url = reverse('register')
        data = {
            "name": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        new_user = User.objects.get(email="newuser@example.com")
        self.assertTrue(check_password("newpassword123", new_user.password))

    def test_register_user_missing_fields(self):
        url = reverse('register')
        data = {"name": "user2"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_list_users_requires_auth(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertTrue(any(u['email'] == self.user.email for u in response.data['users']))

    def test_get_user_detail(self):
        url = reverse('user-detail', args=[self.user.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_user_detail_not_found(self):
        url = reverse('user-detail', args=[9999])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_delete_user_requires_admin(self):
        url = reverse('delete-user', args=[self.user.name])
        # bez auth
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # auth jako zwykły user
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # auth jako admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(name=self.user.name).exists())

    def test_cannot_delete_admin(self):
        url = reverse('delete-user', args=[self.admin.name])
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)
