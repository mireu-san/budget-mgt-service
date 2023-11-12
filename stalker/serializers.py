from rest_framework import serializers
from .models import Expenditure, Category


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
