from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.conf import settings


class BudgetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserBudget(models.Model):
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    period_start = models.DateField()
    period_end = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.amount}"

    @staticmethod
    def get_total_user_budget_for_period(user, start_date, end_date):
        return UserBudget.objects.filter(
            user=user, period_start__gte=start_date, period_end__lte=end_date
        ).aggregate(total=Sum("amount"))["total"]
