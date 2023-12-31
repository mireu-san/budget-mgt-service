from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expenditure, UserPreferences
from .serializers import ExpenditureSerializer, UserPreferencesSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Avg
from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from calendar import monthrange
from budget.models import UserBudget

import datetime


class ExpenditureList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 쿼리 파라미터에서 최소 및 최대 금액을 가져옵니다.
        min_amount = request.query_params.get("min_amount")
        max_amount = request.query_params.get("max_amount")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        category_id = request.query_params.get("category")

        # 필터 조건을 생성합니다.
        filters = Q(user=request.user)
        if min_amount is not None:
            filters &= Q(amount__gte=min_amount)
        if max_amount is not None:
            filters &= Q(amount__lte=max_amount)
        if start_date:
            start_date = parse_datetime(start_date)
            filters &= Q(date__gte=start_date)
        if end_date:
            end_date = parse_datetime(end_date)
            filters &= Q(date__lte=end_date)
        if category_id:
            filters &= Q(category_id=category_id)

        # 필터 조건에 맞는 지출 목록을 조회합니다.
        expenditures = Expenditure.objects.filter(filters)
        total_expenditure = (
            expenditures.exclude(exclude_from_total=True).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

        serializer = ExpenditureSerializer(expenditures, many=True)
        return Response(
            {"expenditures": serializer.data, "total_expenditure": total_expenditure}
        )

    def post(self, request):
        serializer = ExpenditureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenditureDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Expenditure, pk=pk, user=user)

    def get(self, request, pk):
        expenditure = self.get_object(pk, request.user)
        serializer = ExpenditureSerializer(expenditure)
        return Response(serializer.data)

    def put(self, request, pk):
        expenditure = self.get_object(pk, request.user)
        serializer = ExpenditureSerializer(expenditure, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expenditure = self.get_object(pk, request.user)
        expenditure.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 오늘 지출 추천, 안내
class TodaysExpenditureRecommendation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        current_month_budgets = UserBudget.objects.filter(
            user=user, period_start__lte=today, period_end__gte=today
        )

        if not current_month_budgets.exists():
            return Response(
                {"error": "No monthly budget set for this month."},
                status=status.HTTP_404_NOT_FOUND,
            )

        monthly_budget = current_month_budgets.aggregate(Sum("amount"))["amount__sum"]
        minimum_daily_budget = 1000  # Example minimum daily budget
        start_of_month = today.replace(day=1)
        end_of_month = datetime.date(
            today.year, today.month, monthrange(today.year, today.month)[1]
        )
        days_remaining = (end_of_month - today).days + 1

        spent_so_far = (
            Expenditure.objects.filter(
                user=user, date__gte=start_of_month, date__lt=today
            )
            .exclude(exclude_from_total=True)
            .aggregate(Sum("amount"))["amount__sum"]
            or 0
        )

        remaining_budget = max(monthly_budget - spent_so_far, 0)
        daily_budget = max(remaining_budget / days_remaining, minimum_daily_budget)

        user_preferences = UserPreferences.objects.get(user=user)
        monthly_income = user_preferences.monthly_income
        saving_goal = user_preferences.saving_goal

        adjusted_budget = monthly_income - saving_goal

        category_expenditure_ratios = (
            Expenditure.objects.filter(
                user=user,
                date__range=[start_of_month, today - datetime.timedelta(days=1)],
            )
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by()
        )

        total_past_expenditure = sum(
            item["total"] for item in category_expenditure_ratios
        )
        category_recommendations = [
            {
                "category": item["category"],
                "recommended_amount": (item["total"] / total_past_expenditure)
                * adjusted_budget,
            }
            for item in category_expenditure_ratios
        ]

        return Response(
            {
                "date": today,
                "recommended_total_expenditure": daily_budget,
                "category_recommendations": category_recommendations,
            }
        )


class TodaysExpenditureOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        todays_expenditures = Expenditure.objects.filter(user=user, date__date=today)

        total_spent_today = (
            todays_expenditures.aggregate(Sum("amount"))["amount__sum"] or 0
        )
        user_preferences = UserPreferences.objects.get(user=user)
        monthly_income = user_preferences.monthly_income
        saving_goal = user_preferences.saving_goal

        recommended_budget = monthly_income - saving_goal
        risk_percentage = (
            (total_spent_today / recommended_budget - 1) * 100
            if recommended_budget
            else 0
        )

        return Response(
            {
                "date": today,
                "total_spent_today": total_spent_today,
                "risk_percentage": risk_percentage,
            }
        )


class UserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        preferences = get_object_or_404(UserPreferences, user=request.user)
        serializer = UserPreferencesSerializer(preferences)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserPreferencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        preferences = get_object_or_404(UserPreferences, user=request.user)
        serializer = UserPreferencesSerializer(
            preferences, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ExpenditureStatistics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            today = now().date()
            start_of_this_month = today.replace(day=1)
            start_of_last_month = (start_of_this_month - timedelta(days=1)).replace(
                day=1
            )
            end_of_last_month = start_of_this_month - timedelta(days=1)
            same_day_last_week = today - timedelta(days=7)

            # 이번 달 지출 쿼리셋
            this_month_expenditure = (
                Expenditure.objects.filter(
                    user=user, date__range=[start_of_this_month, today]
                )
                .values("category__name")
                .annotate(total=Sum("amount"))
            )

            # 이달 지출 내역이 없을 시 예외처리
            if not this_month_expenditure.exists():
                return Response(
                    {"error": "이 달의 데이터 통계 집계중입니다. 나중에 다시 확인해주세요."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # 지난 달 동일 기간 지출 쿼리셋
            last_month_expenditure = (
                Expenditure.objects.filter(
                    user=user, date__range=[start_of_last_month, end_of_last_month]
                )
                .values("category__name")
                .annotate(total=Sum("amount"))
            )

            # 지난 주 동일 요일 지출 및 이번 요일 지출
            last_week_same_day_expenditure = (
                Expenditure.objects.filter(
                    user=user, date__date=same_day_last_week
                ).aggregate(total=Sum("amount"))["total"]
                or 0
            )

            this_day_expenditure = (
                Expenditure.objects.filter(user=user, date__date=today).aggregate(
                    total=Sum("amount")
                )["total"]
                or 0
            )

            # 모든 사용자의 평균 지출
            average_user_expenditure = (
                Expenditure.objects.filter(date__range=[start_of_this_month, today])
                .values("user")
                .annotate(total=Sum("amount"))
                .aggregate(average=Avg("total"))["average"]
                or 0
            )

            # 각 카테고리별 지난 달 대비 이번 달 지출 비율 계산
            expenditure_comparison = []
            for category in this_month_expenditure:
                category_name = category["category__name"]
                this_month_total = category["total"]
                last_month_total = next(
                    (
                        item
                        for item in last_month_expenditure
                        if item["category__name"] == category_name
                    ),
                    {},
                ).get("total", 0)

                change_rate = (
                    ((this_month_total - last_month_total) / last_month_total * 100)
                    if last_month_total
                    else 0
                )
                expenditure_comparison.append(
                    {
                        "category": category_name,
                        "last_month": last_month_total,
                        "this_month": this_month_total,
                        "change_rate": change_rate,
                    }
                )

            day_comparison_rate = (
                (
                    (this_day_expenditure - last_week_same_day_expenditure)
                    / last_week_same_day_expenditure
                    * 100
                )
                if last_week_same_day_expenditure
                else 0
            )
            user_comparison_rate = (
                (this_day_expenditure / average_user_expenditure * 100)
                if average_user_expenditure
                else 0
            )

            # 결과 반환
            return Response(
                {
                    "monthly_comparison": expenditure_comparison,
                    "day_comparison_rate": day_comparison_rate,
                    "user_comparison_rate": user_comparison_rate,
                }
            )

        except ValueError as e:
            # 잘못된 날짜 입력에 대한 오류 처리
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 서버 내부 오류 처리
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
