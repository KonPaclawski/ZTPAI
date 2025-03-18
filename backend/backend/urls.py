from django.urls import path
from .views import UserListView, UserDetailView
from .budget_view import BudgetDetailView, BudgetListView

urlpatterns = [
    path("api/users/", UserListView.as_view(), name="user-list"),  
    path("api/users/<int:user_id>/", UserDetailView.as_view(), name="user-detail"),
    path("api/budgets/", BudgetListView.as_view(), name="budget_list"),
    path("api/budgets/<int:budget_id>/", BudgetDetailView.as_view(), name="budget_detail"),  
]
