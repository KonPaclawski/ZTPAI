from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from backend.backend.models import Budget, Category, Payment

User = get_user_model()

class BudgetAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
        email='testuser@example.com',
        name='Test User',
        password='testpass'
    )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.budget_list_url = reverse('budget-list')
        self.budget_detail_url = lambda pk: reverse('budget-detail', args=[pk]) 


    def test_get_empty_budget_list(self):
        response = self.client.get(self.budget_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'budgets': []})

    def test_create_budget_with_categories_and_payments(self):
        data = {
            "title": "Test Budget",
            "categories": [
                {
                    "name": "Food",
                    "payments": [
                        {"title": "Groceries", "amount": "100", "date": "2025-05-29"},
                        {"title": "Restaurant", "amount": "50", "date": "2025-05-28"}
                    ]
                },
                {
                    "name": "Transport",
                    "payments": []
                }
            ]
        }
        response = self.client.post(self.budget_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('budget', response.data)
        self.assertEqual(response.data['budget']['title'], "Test Budget")
        self.assertEqual(len(response.data['categories']), 2)
        self.assertEqual(len(response.data['payments']), 2) 

        budget_id = response.data['budget']['id']
        budget = Budget.objects.get(id=budget_id)
        self.assertEqual(budget.title, "Test Budget")
        self.assertEqual(budget.categories.count(), 2)
        self.assertEqual(Payment.objects.filter(budget=budget).count(), 2)

    def test_get_budget_detail(self):
        budget = Budget.objects.create(title="My Budget", user=self.user)
        category = Category.objects.create(name="Bills", budget=budget, user=self.user)
        payment = Payment.objects.create(
            budget=budget,
            category=category,
            user=self.user,
            payment_title="Electricity",
            amount="120",
            date="2025-05-27"
        )

        response = self.client.get(self.budget_detail_url(budget.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], budget.id)
        self.assertEqual(response.data['title'], budget.title)
        self.assertEqual(len(response.data['categories']), 1)
        cat = response.data['categories'][0]
        self.assertEqual(cat['id'], category.id)
        self.assertEqual(cat['name'], "Bills")
        self.assertEqual(len(cat['payments']), 1)
        pay = cat['payments'][0]
        self.assertEqual(pay['payment_title'], "Electricity")
        self.assertEqual(str(pay['amount']), "120.00")

    def test_get_budget_detail_not_found(self):
        response = self.client.get(self.budget_detail_url(9999))  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_create_budget_missing_title(self):
        data = {"categories": []}
        response = self.client.post(self.budget_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_category_missing_name(self):
        data = {
            "title": "Budget",
            "categories": [
                {"payments": []}  
            ]
        }
        response = self.client.post(self.budget_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_payment_missing_fields(self):
        data = {
            "title": "Budget",
            "categories": [
                {
                    "name": "Cat1",
                    "payments": [
                        {"amount": "100"} 
                    ]
                }
            ]
        }
        response = self.client.post(self.budget_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
