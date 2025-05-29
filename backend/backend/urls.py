from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import UserListView, UserDetailView, RegisterUserView, DeleteUserView
from .budget_view import BudgetListView, BudgetDetailView
from .login_view import LoginView, LogoutView, CustomTokenRefreshView
from .note_view import NoteView

schema_view = get_schema_view(
   openapi.Info(
      title="Budget API",
      default_version='v1',
      description="API do zarządzania budżetem",
      contact=openapi.Contact(email="twoj.email@example.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

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

    re_path(r'^api/docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
