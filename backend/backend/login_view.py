import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "Missing email or password"}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

            if not check_password(password, user.password):
                return JsonResponse({"error": "Invalid credentials"}, status=401)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = JsonResponse({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role
                }
            })

            # Set HttpOnly cookies
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,   # True w produkcji (HTTPS)
                samesite='Lax',
                path='/',
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/api/token/refresh/',
            )

            return response

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(View):
    def post(self, request):
        response = JsonResponse({"message": "Logged out"})
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/api/token/refresh/')
        return response

@method_decorator(csrf_exempt, name="dispatch")
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return JsonResponse({"error": "No refresh token provided"}, status=401)

        data = {"refresh": refresh_token}
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse({"error": "Invalid refresh token"}, status=401)

        access_token = serializer.validated_data['access']

        response = JsonResponse({"access": access_token})
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/',
        )
        return response
