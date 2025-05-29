import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from ..models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    @swagger_auto_schema(
        operation_description="Logowanie użytkownika",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email użytkownika'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Hasło użytkownika'),
            },
        ),
        responses={
            200: openapi.Response(
                description="Logowanie udane",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'role': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            400: "Brak emaila lub hasła / Niepoprawny JSON",
            401: "Niepoprawne dane logowania"
        }
    )
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

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
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
    @swagger_auto_schema(
        operation_description="Wylogowanie użytkownika",
        responses={200: "Wylogowano pomyślnie"}
    )
    def post(self, request):
        response = JsonResponse({"message": "Logged out"})
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/api/token/refresh/')
        return response

@method_decorator(csrf_exempt, name="dispatch")
class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Odświeżanie tokena dostępu",
        responses={
            200: openapi.Response(
                description="Token odświeżony",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: "Brak lub niepoprawny token odświeżający"
        }
    )
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
