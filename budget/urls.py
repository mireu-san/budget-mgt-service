from django.urls import path
from .views import (
    BudgetCategoryList,
    UserBudgetCreate,
    BudgetRecommendation,
)

urlpatterns = [
    path("categories/", BudgetCategoryList.as_view(), name="category-list"),
    path("create/", UserBudgetCreate.as_view(), name="budget-create"),
    path(
        "recommendation/",
        BudgetRecommendation.as_view(),
        name="budget-recommendation",
    ),
]
