from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .models import Expenditure
from budget.models import UserBudget
from discord import send_discord_notification
from django.db.models import Sum

User = get_user_model()


@shared_task
def send_budget_exceed_alerts():
    users = User.objects.all()
    for user in users:
        # 사용자별 예산 초과 여부 확인
        if is_budget_exceeded(user):
            message = f"Alert: {user.username}, 지출액이 예산을 초과했습니다! 지출을 조정하세요."

            # Discord 알림 보내기 (사용자별로 Discord Webhook URL 설정 필요)
            webhook_url = user.discord_webhook_url  # 사용자 모델에 webhook URL을 저장해야 합니다.
            send_discord_notification(webhook_url, message)


def is_budget_exceeded(user):
    # 현재 날짜를 기준으로 시작 및 종료 날짜 정의
    today = now().date()
    start_date = today.replace(day=1)  # 이번 달의 시작
    end_date = today  # 현재 날짜

    # 사용자별 지출 및 예산 계산
    total_expenditure = get_total_expenditure_for_user(user, start_date, end_date)
    total_budget = UserBudget.get_total_user_budget_for_period(
        user, start_date, end_date
    )
    return total_expenditure > total_budget if total_budget else False


def get_total_expenditure_for_user(user, start_date, end_date):
    # 사용자별 지출 합계 계산
    return (
        Expenditure.objects.filter(
            user=user, date__gte=start_date, date__lte=end_date
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
