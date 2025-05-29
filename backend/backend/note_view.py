import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Note, Payment
from django.contrib.auth.decorators import login_required

@method_decorator(csrf_exempt, name='dispatch')
class NoteView(View):
    
    def get(self, request, payment_id):
        try:
            note = Note.objects.get(payment__id=payment_id)
            return JsonResponse({"id": note.id, "payment": note.payment.id, "content": note.content})
        except Note.DoesNotExist:
            return JsonResponse({"error": "Note not found"}, status=404)
        
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
