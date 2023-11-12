from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expenditure(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    memo = models.TextField(blank=True, null=True)
    exclude_from_total = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s expenditure on {self.date}"


class UserPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 월 소득
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # 목표 저축액
    saving_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # 지출 스타일
    spending_style = models.CharField(
        max_length=30,
        choices=[
            ("conservative", "Conservative"),
            ("moderate", "Moderate"),
            ("aggressive", "Aggressive"),
        ],
        default="moderate",
    )
    # 주요 지출 카테고리 1
    primary_category_1 = models.ForeignKey(
        Category,
        related_name="primary_category_1",
        on_delete=models.SET_NULL,
        null=True,
    )
    # 주요 지출 카테고리 2
    primary_category_2 = models.ForeignKey(
        Category,
        related_name="primary_category_2",
        on_delete=models.SET_NULL,
        null=True,
    )
    # 단기 목표 저축액
    short_term_savings_goal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    # 장기 목표 저축액
    long_term_savings_goal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    # 소득 범위
    income_range = models.CharField(
        max_length=30,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium",
    )
    # 저축률
    saving_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )  # 퍼센트 표시

    def __str__(self):
        return f"Preferences of {self.user.username}"
