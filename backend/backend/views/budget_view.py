from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from backend.authentication import CookieJWTAuthentication
from ..models import Budget, Category, Payment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BudgetListView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Pobierz listę budżetów użytkownika wraz z kategoriami i płatnościami",
        responses={200: openapi.Response(
            description="Lista budżetów",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "budgets": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "title": openapi.Schema(type=openapi.TYPE_STRING),
                                "categories": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                            "name": openapi.Schema(type=openapi.TYPE_STRING),
                                            "payments": openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_OBJECT,
                                                    properties={
                                                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                                        "payment_title": openapi.Schema(type=openapi.TYPE_STRING),
                                                        "amount": openapi.Schema(type=openapi.TYPE_STRING),
                                                        "date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                                                    }
                                                )
                                            )
                                        }
                                    )
                                )
                            }
                        )
                    )
                }
            )
        )}
    )
    def get(self, request):
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

    @swagger_auto_schema(
        operation_description="Utwórz nowy budżet z kategoriami i płatnościami",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Tytuł budżetu'),
                'categories': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Lista kategorii",
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nazwa kategorii'),
                            'payments': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                description='Lista płatności w kategorii',
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Tytuł płatności'),
                                        'amount': openapi.Schema(type=openapi.TYPE_STRING, description='Kwota płatności'),
                                        'date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Data płatności'),
                                    }
                                )
                            )
                        }
                    )
                )
            }
        ),
        responses={
            201: openapi.Response(description="Budżet utworzony pomyślnie"),
            400: "Błędne dane wejściowe"
        }
    )
    def post(self, request):
        data = request.data
        title = data.get("title")
        categories_data = data.get("categories", [])

        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

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


class BudgetDetailView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Pobierz szczegóły budżetu po ID, wraz z kategoriami i płatnościami",
        responses={
            200: openapi.Response(
                description="Szczegóły budżetu",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "categories": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "payments": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                                "payment_title": openapi.Schema(type=openapi.TYPE_STRING),
                                                "amount": openapi.Schema(type=openapi.TYPE_STRING),
                                                "date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                                            }
                                        )
                                    )
                                }
                            )
                        )
                    }
                )
            ),
            404: "Budżet nie znaleziony"
        }
    )
    def get(self, request, pk):
        try:
            budget = Budget.objects.prefetch_related('categories__payments').get(pk=pk, user=request.user)
        except Budget.DoesNotExist:
            return Response({"error": "Budget not found"}, status=status.HTTP_404_NOT_FOUND)

        categories_data = []
        for category in budget.categories.all():
            payments = list(category.payments.values("id", "payment_title", "amount", "date"))
            categories_data.append({
                "id": category.id,
                "name": category.name,
                "payments": payments
            })

        data = {
            "id": budget.id,
            "title": budget.title,
            "categories": categories_data
        }

        return Response(data, status=status.HTTP_200_OK)
