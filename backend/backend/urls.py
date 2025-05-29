from django.urls import path
from .views import UserListView, UserDetailView, RegisterUserView, DeleteUserView
from .budget_view import BudgetListView, BudgetDetailView
from .login_view import LoginView, LogoutView, CustomTokenRefreshView
from .note_view import NoteView

urlpatterns = [
    path("api/users/", UserListView.as_view(), name="user-list"),  
    path("api/users/<int:user_id>/", UserDetailView.as_view(), name="user-detail"),

    path("api/budgets/", BudgetListView.as_view(), name="budget-list"),
    path('api/budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),

    path("api/login/", LoginView.as_view(), name="login"),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    path("api/register/", RegisterUserView.as_view(), name="register"),
    path('api/admin/delete-user/<str:username>/', DeleteUserView.as_view(), name='delete-user'),

    path('api/notes/', NoteView.as_view(), name='create_note'),
    path('api/notes/<int:payment_id>/', NoteView.as_view(), name='note-detail'),
    
    path("api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]