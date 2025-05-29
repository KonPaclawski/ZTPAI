import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models import Note, Payment
from django.contrib.auth.decorators import login_required
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@method_decorator(csrf_exempt, name='dispatch')
class NoteView(View):

    @swagger_auto_schema(
        operation_description="Pobierz notatkę powiązaną z podanym payment_id",
        responses={
            200: openapi.Response(
                description="Notatka",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "payment": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "content": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            404: "Notatka nie znaleziona"
        },
        manual_parameters=[
            openapi.Parameter(
                'payment_id', openapi.IN_PATH, description="ID płatności", type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, payment_id):
        try:
            note = Note.objects.get(payment__id=payment_id)
            return JsonResponse({"id": note.id, "payment": note.payment.id, "content": note.content})
        except Note.DoesNotExist:
            return JsonResponse({"error": "Note not found"}, status=404)

    @swagger_auto_schema(
        operation_description="Utwórz lub zaktualizuj notatkę powiązaną z płatnością",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["payment_id", "content"],
            properties={
                "payment_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID płatności"),
                "content": openapi.Schema(type=openapi.TYPE_STRING, description="Treść notatki"),
            },
        ),
        responses={
            201: openapi.Response(
                description="Notatka utworzona lub zaktualizowana",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "payment": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "content": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Błędne dane",
            404: "Płatność nie znaleziona"
        }
    )
    def post(self, request):
        try:
            data = json.loads(request.body)
            payment_id = data.get("payment_id")
            content = data.get("content")

            if not payment_id or content is None:
                return JsonResponse({"error": "Missing payment_id or content"}, status=400)

            payment = Payment.objects.get(id=payment_id)

            note, created = Note.objects.update_or_create(
                payment=payment,
                defaults={"content": content}
            )

            return JsonResponse({"id": note.id, "payment": note.payment.id, "content": note.content}, status=201)
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @swagger_auto_schema(
        operation_description="Aktualizuj notatkę powiązaną z podanym payment_id",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["content"],
            properties={
                "content": openapi.Schema(type=openapi.TYPE_STRING, description="Nowa treść notatki"),
            },
        ),
        responses={
            200: openapi.Response(
                description="Notatka zaktualizowana",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "payment": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "content": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Błędne dane",
            404: "Notatka nie znaleziona"
        },
        manual_parameters=[
            openapi.Parameter(
                'payment_id', openapi.IN_PATH, description="ID płatności", type=openapi.TYPE_INTEGER
            )
        ]
    )
    def put(self, request, payment_id):
        try:
            data = json.loads(request.body)
            content = data.get("content")

            if content is None:
                return JsonResponse({"error": "Missing content"}, status=400)

            note = Note.objects.get(payment__id=payment_id)
            note.content = content
            note.save()
            return JsonResponse({"id": note.id, "payment": note.payment.id, "content": note.content})
        except Note.DoesNotExist:
            return JsonResponse({"error": "Note not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
