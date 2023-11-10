from rest_framework import serializers
from users.models import User
from budget.models import BudgetCategory, UserBudget


class SwaggerSignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class SwaggerSignupResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class SwaggerLoginRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class SwaggerBudgetCategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = ["id", "name"]


class SwaggerUserBudgetCreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBudget
        fields = ["category", "amount", "period_start", "period_end"]


class SwaggerUserBudgetCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBudget
        fields = ["id", "category", "amount", "period_start", "period_end"]


class SwaggerBudgetRecommendationRequestSerializer(serializers.Serializer):
    total_budget = serializers.DecimalField(max_digits=10, decimal_places=2)


class SwaggerBudgetRecommendationResponseSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
