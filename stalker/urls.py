from django.urls import path
from .views import (
    ExpenditureList,
    ExpenditureDetail,
    TodaysExpenditureRecommendation,
    TodaysExpenditureOverview,
)

urlpatterns = [
    path("expenditures/", ExpenditureList.as_view(), name="expenditure-list"),
    path(
        "expenditures/<int:pk>/", ExpenditureDetail.as_view(), name="expenditure-detail"
    ),
    path(
        "expenditure/recommendation/",
        TodaysExpenditureRecommendation.as_view(),
        name="expenditure-recommendation",
    ),
    path(
        "expenditure/overview/",
        TodaysExpenditureOverview.as_view(),
        name="expenditure-overview",
    ),
]
