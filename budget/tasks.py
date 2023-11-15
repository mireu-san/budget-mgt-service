from celery import shared_task
from django.utils.timezone import now
from .models import UserBudget
from django.contrib.auth import get_user_model
from discord import send_discord_notification

User = get_user_model()


@shared_task
def send_daily_budget_recommendations():
    users = User.objects.all()
    for user in users:
        # 사용자별 일일 예산 추천 로직
        recommended_budget = calculate_daily_budget_for_user(user)

        # Discord 알림 메시지 생성
        message = (
            f"{user.username}, your recommended daily budget is {recommended_budget}"
        )

        # Discord 알림 보내기 (사용자별로 Discord Webhook URL 설정 필요)
        webhook_url = user.discord_webhook_url  # 사용자 모델에 webhook URL을 저장해야 합니다.
        send_discord_notification(webhook_url, message)


def calculate_daily_budget_for_user(user):
    # 현재 날짜를 기준으로 시작 및 종료 날짜 정의
    today = now().date()
    start_date = today.replace(day=1)  # 이번 달의 시작
    end_date = today  # 현재 날짜

    # 사용자별 전체 예산 계산
    total_budget = UserBudget.get_total_user_budget_for_period(
        user, start_date, end_date
    )
    days_in_month = (end_date - start_date).days + 1  # 이번 달의 총 일수 계산
    return total_budget / days_in_month if total_budget else 0
