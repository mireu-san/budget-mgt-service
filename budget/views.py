from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from .models import BudgetCategory, UserBudget
from .serializers import BudgetCategorySerializer, UserBudgetSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from swagger import *


class BudgetCategoryList(APIView):
    @swagger_auto_schema(
        operation_id="카테고리 목록 조회",
        operation_description="모든 예산 카테고리 목록을 반환합니다.",
        responses={200: SwaggerBudgetCategoryResponseSerializer(many=True)},
    )
    def get(self, request, format=None):
        categories = BudgetCategory.objects.all()
        serializer = BudgetCategorySerializer(categories, many=True)
        return Response(serializer.data)


class UserBudgetCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="예산 생성",
        operation_description="사용자가 새로운 예산을 생성합니다.",
        request_body=SwaggerUserBudgetCreateRequestSerializer,
        responses={201: SwaggerUserBudgetCreateResponseSerializer},
    )
    def post(self, request, format=None):
        serializer = UserBudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BudgetRecommendation(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="예산 추천",
        operation_description="전체 예산에 대한 카테고리별 예산 분배를 추천합니다.",
        request_body=SwaggerBudgetRecommendationRequestSerializer,
        responses={200: SwaggerBudgetRecommendationResponseSerializer},
    )
    def post(self, request, format=None):
        total_budget = request.data.get("total_budget")
        if not total_budget:
            return Response({"error": "전체 예산이 요구됩니다."}, status=400)

        # 카테고리별 평균 예산 비율 계산
        average_budgets = UserBudget.objects.values("category").annotate(
            average_amount=Avg("amount")
        )
        total_average = sum([budget["average_amount"] for budget in average_budgets])

        # 각 카테고리에 대한 추천 예산 계산
        recommended_budgets = []
        for budget in average_budgets:
            category = budget["category"]
            avg_amount = budget["average_amount"]
            recommended_amount = (avg_amount / total_average) * total_budget
            recommended_budgets.append(
                {"category": category, "amount": recommended_amount}
            )

        return Response(recommended_budgets)
