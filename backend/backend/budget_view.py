import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Budget  
from .models import User

@method_decorator(csrf_exempt, name='dispatch')
class BudgetListView(View):
    def get(self, request):
        budgets = list(Budget.objects.values())  
        return JsonResponse({"budgets": budgets}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            required_fields = ["title", "category", "payment_title", "amount", "user_id"]
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "Missing fields"}, status=400)

            # Używamy `user_id` do odnalezienia użytkownika
            user = User.objects.get(id=data["user_id"])
            
            new_budget = Budget.objects.create(
                title=data["title"],
                category=data["category"],
                payment_title=data["payment_title"],
                amount=data["amount"],
                user=user  # Używamy obiektu `user`
            )

            return JsonResponse({"message": "Budget created", "budget": {
                "id": new_budget.id,
                "title": new_budget.title,
                "category": new_budget.category,
                "payment_title": new_budget.payment_title,
                "amount": new_budget.amount,
                "user_id": new_budget.user.id  # Zwracamy `user_id`, nie `user`
            }}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class UserBudgetListView(View):
    def get(self, request, user_id):
        budgets = list(Budget.objects.filter(user_id=user_id).values())
        return JsonResponse({"budgets": budgets}, status=200)

    def post(self, request, user_id):
        try:
            data = json.loads(request.body)
            required_fields = ["title", "category", "payment_title", "amount"]
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "Missing fields"}, status=400)

            # Sprawdzamy, czy użytkownik istnieje
            user = User.objects.get(id=user_id)

            new_budget = Budget.objects.create(
                title=data["title"],
                category=data["category"],
                payment_title=data["payment_title"],
                amount=data["amount"],
                user=user  # Używamy obiektu `user`
            )

            return JsonResponse({"message": "Budget created", "budget": {
                "id": new_budget.id,
                "title": new_budget.title,
                "category": new_budget.category,
                "payment_title": new_budget.payment_title,
                "amount": new_budget.amount,
                "user_id": new_budget.user.id  # Zwracamy `user_id`, nie `user`
            }}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
