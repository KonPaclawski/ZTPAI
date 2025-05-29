from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from backend.models import Payment, Note

User = get_user_model()

class NoteViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name="TestUser", email="test@example.com", password="testpass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.payment = Payment.objects.create(user=self.user, amount=100, description="Test payment")

    def test_get_note_not_found(self):
        url = reverse('note-detail', args=[self.payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], "Note not found")

    def test_create_note(self):
        url = reverse('create_note')
        data = {
            "payment_id": self.payment.id,
            "content": "This is a test note."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['content'], "This is a test note.")
        self.assertEqual(response.json()['payment'], self.payment.id)

    def test_update_note_via_post(self):
        note = Note.objects.create(payment=self.payment, content="Old content")

        url = reverse('create_note')
        data = {
            "payment_id": self.payment.id,
            "content": "Updated content via POST"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['content'], "Updated content via POST")
        self.assertEqual(response.json()['id'], note.id) 

    def test_get_note_success(self):
        note = Note.objects.create(payment=self.payment, content="Note content")
        url = reverse('note-detail', args=[self.payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['content'], "Note content")
        self.assertEqual(response.json()['payment'], self.payment.id)

    def test_put_update_note_success(self):
        note = Note.objects.create(payment=self.payment, content="Initial content")
        url = reverse('note-detail', args=[self.payment.id])
        data = {
            "content": "Updated content via PUT"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['content'], "Updated content via PUT")

    def test_put_update_note_missing_content(self):
        note = Note.objects.create(payment=self.payment, content="Initial content")
        url = reverse('note-detail', args=[self.payment.id])
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Missing content', response.json().get('error', ''))

    def test_put_update_note_not_found(self):
        url = reverse('note-detail', args=[9999]) 
        data = {"content": "Some content"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Note not found', response.json().get('error', ''))
