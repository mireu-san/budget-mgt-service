from rest_framework import serializers
from .models import BudgetCategory, UserBudget


class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = ["id", "name"]


class UserBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBudget
        fields = ["id", "category", "amount", "start_date", "end_date"]

    def create(self, validated_data):
        # user 필드를 create 메소드에서 처리
        user = self.context["request"].user
        return UserBudget.objects.create(user=user, **validated_data)
