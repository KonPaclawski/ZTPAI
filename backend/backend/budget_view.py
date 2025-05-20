from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Budget 

class BudgetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user).values()
        return Response({"budgets": list(budgets)}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        required_fields = ["title", "category", "payment_title", "amount"]
        if not all(field in data for field in required_fields):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        budget = Budget.objects.create(
            title=data["title"],
            category=data["category"],
            payment_title=data["payment_title"],
            amount=data["amount"],
            user=request.user 
        )

        return Response({
            "message": "Budget created",
            "budget": {
                "id": budget.id,
                "title": budget.title,
                "category": budget.category,
                "payment_title": budget.payment_title,
                "amount": budget.amount,
                "user_id": budget.user.id
            }
        }, status=status.HTTP_201_CREATED)
