from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Budget, Payment

class BudgetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user).values("id", "title", "category")
        return Response({"budgets": list(budgets)}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        required_fields = ["title", "category", "payment_title", "amount"]
        if not all(field in data for field in required_fields):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Budget
        budget = Budget.objects.create(
            title=data["title"],
            category=data["category"],
            user=request.user
        )

        # Create Payment linked to the budget
        payment = Payment.objects.create(
            budget=budget,
            payment_title=data["payment_title"],
            amount=data["amount"],
            date=data.get("date")  # Optional; you can default this if missing
        )

        return Response({
            "message": "Budget and payment created",
            "budget": {
                "id": budget.id,
                "title": budget.title,
                "category": budget.category,
                "user_id": budget.user.id
            },
            "payment": {
                "id": payment.id,
                "title": payment.payment_title,
                "amount": str(payment.amount),
                "date": str(payment.date)
            }
        }, status=status.HTTP_201_CREATED)
