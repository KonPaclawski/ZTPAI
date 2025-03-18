import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


users = [
    {"id": 1, "name": "jano", "email": "jan@gmail.com"},
    {"id": 2, "name": "anna", "email": "anna@gmail.com"},
]
next_id = 3  

@method_decorator(csrf_exempt, name='dispatch')
class UserListView(View):
    def get(self, request):
        return JsonResponse({"users": users}, status=200)

    def post(self, request):
        global next_id
        try:
            data = json.loads(request.body)
            if "name" not in data or "email" not in data:
                return JsonResponse({"error": "Missing field"}, status=400)

            new = {"id": next_id, "name": data["name"], "email": data["email"]}
            users.append(new)
            next_id += 1
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(View):
    def get_user(self, user_id):
        for user in users:
            if user["id"] == user_id:
                return user
        return None

    def get(self, request, user_id):
        user = self.get_user(user_id)
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)
        return JsonResponse(user, status=200)

    def put(self, request, user_id):
        user = self.get_user(user_id)
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = json.loads(request.body)
            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])

            return JsonResponse({"message": "User updated", "user": user}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, user_id):
        global users
        user = self.get_user(user_id)
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        users = [u for u in users if u["id"] != user_id]
