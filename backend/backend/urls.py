from django.urls import path
from .views import UserListView, UserDetailView, RegisterUserView
from .budget_view import BudgetListView
from .login_view import LoginView
from .token_refresh_view import CustomTokenRefreshView

urlpatterns = [
    path("api/users/", UserListView.as_view(), name="user-list"),  
    path("api/users/<int:user_id>/", UserDetailView.as_view(), name="user-detail"),

    path("api/budgets/", BudgetListView.as_view(), name="budget-list"),

    path("api/login/", LoginView.as_view(), name="login"),
    path("api/register/", RegisterUserView.as_view(), name="register"),

    path("api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]