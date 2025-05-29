from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views.views import UserListView, UserDetailView, RegisterUserView, DeleteUserView
from .views.budget_view import BudgetListView, BudgetDetailView
from .views.login_view import LoginView, LogoutView, CustomTokenRefreshView
from .views.note_view import NoteView

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
    path("api/v1/users/", UserListView.as_view(), name="user-list"),  
    path("api/v1/users/<int:user_id>/", UserDetailView.as_view(), name="user-detail"),

    path("api/v1/budgets/", BudgetListView.as_view(), name="budget-list"),
    path('api/v1/budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),

    path("api/v1/login/", LoginView.as_view(), name="login"),
    path('api/v1/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    path("api/v1/register/", RegisterUserView.as_view(), name="register"),
    path('api/v1/admin/delete-user/<str:username>/', DeleteUserView.as_view(), name='delete-user'),

    path('api/v1/notes/', NoteView.as_view(), name='create_note'),
    path('api/v1/notes/<int:payment_id>/', NoteView.as_view(), name='note-detail'),

    re_path(r'^api/v1/docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
