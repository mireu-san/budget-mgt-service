from django.urls import path
from .views import ExpenditureList, ExpenditureDetail

urlpatterns = [
    path("expenditures/", ExpenditureList.as_view(), name="expenditure-list"),
    path(
        "expenditures/<int:pk>/", ExpenditureDetail.as_view(), name="expenditure-detail"
    ),
]
