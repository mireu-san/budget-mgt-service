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
