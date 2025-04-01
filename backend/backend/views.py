import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User  

@method_decorator(csrf_exempt, name="dispatch")
class UserListView(View):

    def get(self, request):
        users = list(User.objects.values("id", "name", "email"))  
        return JsonResponse({"users": users}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if "name" not in data or "email" not in data or "password" not in data:
                return JsonResponse({"error": "Missing field"}, status=400)

            new_user = User.objects.create(
                name=data["name"],
                email=data["email"],
                password=data["password"] 
            )
            new_user.save(force_insert=True)
            return JsonResponse(
                {"message": "User registered successfully!", "user_id": new_user.id},
                status=201
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(View):

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        user = self.get_user(user_id)
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        return JsonResponse({"id": user.id, "name": user.name, "email": user.email}, status=200)
