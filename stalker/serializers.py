from rest_framework import serializers
from .models import Expenditure, Category, UserPreferences


class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        fields = [
            "id",
            "user",
            "date",
            "amount",
            "category",
            "memo",
            "exclude_from_total",
        ]


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = [
            "user",
            "monthly_income",
            "saving_goal",
            "spending_style",
            "primary_category_1",
            "primary_category_2",
            "short_term_savings_goal",
            "long_term_savings_goal",
            "income_range",
            "saving_rate",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
