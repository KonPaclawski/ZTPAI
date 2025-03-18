import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

budgets = [
    {"id": 1, "title": "Mieszkanie", "category": "Rachunki", "payment_title": "Czynsz", "amount": 2500, "user_id": 1},
    {"id": 2, "title": "Samochód", "category": "Transport", "payment_title": "Naprawa silnika", "amount": 1800, "user_id": 2},
]
next_budget_id = 3  

@method_decorator(csrf_exempt, name='dispatch')
class BudgetListView(View):
    def get(self, request):
        return JsonResponse({"budgets": budgets}, status=200)

    def post(self, request):
        global next_budget_id
        try:
            data = json.loads(request.body)
            required_fields = ["title", "category", "payment_title", "amount", "user_id"]
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "Missing fields"}, status=400)

            new_budget = {
                "id": next_budget_id,"title": data["title"],"category": data["category"],
                "payment_title": data["payment_title"],"amount": data["amount"],"user_id": data["user_id"]
            }
            budgets.append(new_budget)
            next_budget_id += 1

            return JsonResponse({"message": "Budget created", "budget": new_budget}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class BudgetDetailView(View):
    def get_budget(self, budget_id):
        for budget in budgets:
            if budget["id"] == budget_id:
                return budget
        return None

    def get(self, request, budget_id):
        budget = self.get_budget(budget_id)
        if not budget:
            return JsonResponse({"error": "Budget not found"}, status=404)
        return JsonResponse(budget, status=200)

    def put(self, request, budget_id):
        budget = self.get_budget(budget_id)
        if not budget:
            return JsonResponse({"error": "Budget not found"}, status=404)

        try:
            data = json.loads(request.body)
            budget["title"] = data.get("title", budget["title"])
            budget["category"] = data.get("category", budget["category"])
            budget["payment_title"] = data.get("payment_title", budget["payment_title"])
            budget["amount"] = data.get("amount", budget["amount"])
            budget["user_id"] = data.get("user_id", budget["user_id"])

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, budget_id):
        global budgets
        budget = self.get_budget(budget_id)
        if not budget:
            return JsonResponse({"error": "Budget not found"}, status=404)

        budgets = [a for a in budgets if a["id"] != budget_id]
