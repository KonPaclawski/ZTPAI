from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Pobierz listę wszystkich użytkowników",
        responses={
            200: openapi.Response(
                description="Lista użytkowników",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "users": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                                },
                            ),
                        )
                    }
                )
            ),
            401: "Brak autoryzacji"
        }
    )
    def get(self, request):
        users = list(User.objects.values("id", "name", "email"))
        return Response({"users": users}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Rejestracja nowego użytkownika",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "email", "password"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Nazwa użytkownika"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email użytkownika"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Hasło użytkownika"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Użytkownik zarejestrowany pomyślnie",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Błędne dane (np. brak wymaganych pól lub email istnieje)"
        }
    )
    def post(self, request):
        data = request.data
    
        if "name" not in data or "email" not in data or "password" not in data:
            return Response({"error": "Missing field"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        role_for = "admin" if data["email"] == "admin@admin.com" else "user"
            
        new_user = User(
            name=data["name"],
            email=data["email"],
            password=make_password(data["password"]),
            role=role_for
        )
        new_user.save()

        refresh = RefreshToken.for_user(new_user)
        return Response({
            "message": "User registered successfully!",
            "user_id": new_user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Pobierz szczegóły użytkownika po ID",
        responses={
            200: openapi.Response(
                description="Szczegóły użytkownika",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            404: "Użytkownik nie znaleziony",
            401: "Brak autoryzacji"
        },
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_PATH, description="ID użytkownika", type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"id": user.id, "name": user.name, "email": user.email}, status=status.HTTP_200_OK)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Usuń użytkownika po nazwie (tylko admin może usuwać)",
        responses={
            204: "Użytkownik usunięty pomyślnie",
            403: "Brak uprawnień do usunięcia użytkownika",
            404: "Użytkownik nie znaleziony",
            401: "Brak autoryzacji"
        },
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_PATH, description="Nazwa użytkownika do usunięcia", type=openapi.TYPE_STRING
            )
        ]
    )
    def delete(self, request, username):
        if not request.user.is_authenticated or request.user.role != "admin":
            return Response({"error": "Nie masz uprawnień."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user_to_delete = User.objects.get(name=username)
            if user_to_delete.role == "admin":
                return Response({"error": "Nie można usunąć innego administratora."}, status=status.HTTP_403_FORBIDDEN)
            user_to_delete.delete()
            return Response({"message": f"Użytkownik '{username}' został usunięty."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Użytkownik nie istnieje."}, status=status.HTTP_404_NOT_FOUND)
