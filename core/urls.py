"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Budget Management API",
        default_version="v1",
        description="예산 관리 서비스 API 입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(url="https://github.com/mireu-san/budget-mgt-service"),
    ),
    public=True,
)

urlpatterns = [
    # swagger
    re_path(
        "^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(r"^$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-root"),
    re_path(
        r"redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc-v1",
    ),
    # url
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/budget/", include("budget.urls")),
    path("api/v1/stalker/", include("stalker.urls")),
]
