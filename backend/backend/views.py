from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = list(User.objects.values("id", "name", "email"))
        return Response({"users": users}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        data = request.data
    
        if "name" not in data or "email" not in data or "password" not in data:
            return Response({"error": "Missing field"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if(data["email"] == "admin@admin.com"):
            role_for = "admin"
        else:
            role_for = "user"
            
        new_user = User(
            name=data["name"],
            email=data["email"],
            password=make_password(data["password"]),
            role=role_for
        )
        new_user.save()
        print("Użytkownik zapisany:", new_user.email)
        refresh = RefreshToken.for_user(new_user)
        return Response({
            "message": "User registered successfully!",
            "user_id": new_user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"id": user.id, "name": user.name, "email": user.email}, status=status.HTTP_200_OK)
