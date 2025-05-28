from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Budget, Category, Payment

class BudgetListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("DEBUG USER:", request.user)
        print("DEBUG AUTH:", request.headers.get("Authorization"))

        budgets = Budget.objects.filter(user=request.user).prefetch_related('categories__payments')

        data = []
        for budget in budgets:
            categories_data = []
            for category in budget.categories.all():
                payments = list(category.payments.values("id", "payment_title", "amount", "date"))
                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "payments": payments
                })

            data.append({
                "id": budget.id,
                "title": budget.title,
                "categories": categories_data
            })

        return Response({"budgets": data}, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        title = data.get("title")
        categories_data = data.get("categories", [])

        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create budget linked to user
        budget = Budget.objects.create(title=title, user=request.user)
        created_categories = []
        created_payments = []

        for cat_data in categories_data:
            cat_name = cat_data.get("name")
            if not cat_name:
                return Response({"error": "Each category must have a name"}, status=status.HTTP_400_BAD_REQUEST)

            category = Category.objects.create(name=cat_name, user=request.user, budget=budget)
            created_categories.append({"id": category.id, "name": category.name})

            for payment_data in cat_data.get("payments", []):
                payment_title = payment_data.get("title")
                amount = payment_data.get("amount")
                date = payment_data.get("date")

                if not payment_title or amount is None:
                    return Response({"error": "Payment title and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

                payment = Payment.objects.create(
                    budget=budget,
                    category=category,
                    user=request.user,
                    payment_title=payment_title,
                    amount=amount,
                    date=date
                )
                created_payments.append({
                    "id": payment.id,
                    "title": payment.payment_title,
                    "amount": str(payment.amount),
                    "date": str(payment.date),
                })

        return Response({
            "message": "Budget, categories and payments created successfully",
            "budget": {"id": budget.id, "title": budget.title},
            "categories": created_categories,
            "payments": created_payments,
        }, status=status.HTTP_201_CREATED)
