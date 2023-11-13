import os
import django
from faker import Faker
import random
from datetime import date  # timedelta (기간 설정시) # pytz 는 직접적으로 다룰 때
from django.utils import timezone
import time  # 실행시간 측정

# 시작 시간 기록
start_time = time.time()

# Django 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# 모델 가져오기
from users.models import User
from budget.models import BudgetCategory, UserBudget
from stalker.models import Category, Expenditure, UserPreferences

# Faker 인스턴스 초기화
fake = Faker()

# 사용자 생성
for _ in range(10):
    username = fake.user_name()
    email = fake.email()
    User.objects.create_user(username=username, email=email, password="test1234")

# 예산 카테고리 생성
budget_categories = ["Food", "Transport", "Entertainment", "Utilities"]
for name in budget_categories:
    _, created = BudgetCategory.objects.get_or_create(name=name)
    if not created:
        print(f"Budget category {name} already exists.")

# 사용자별 예산 할당
for user in User.objects.all():
    for category in BudgetCategory.objects.all():
        UserBudget.objects.create(
            user=user,
            category=category,
            amount=random.uniform(100, 1000),
            period_start=date.today().replace(day=1),
            period_end=date.today(),
        )

# 지출 카테고리 생성
expense_categories = ["Groceries", "Dining Out", "Cinema", "Electricity Bill"]
for name in expense_categories:
    _, created = Category.objects.get_or_create(name=name)
    if not created:
        print(f"Expense category {name} already exists.")

# 사용자별 지출 기록
for user in User.objects.all():
    for _ in range(20):  # 각 사용자당 20개의 지출 기록
        naive_datetime = fake.date_time_this_month()
        aware_datetime = timezone.make_aware(
            naive_datetime, timezone.get_default_timezone()
        )

        Expenditure.objects.create(
            user=user,
            date=aware_datetime,
            amount=random.uniform(10, 200),
            category=random.choice(Category.objects.all()),
            memo=fake.sentence(),
            exclude_from_total=fake.boolean(),
        )

# 사용자 선호도 설정
for user in User.objects.all():
    obj, created = UserPreferences.objects.get_or_create(
        user=user,
        defaults={
            "monthly_income": random.uniform(1000, 5000),
            "saving_goal": random.uniform(100, 1000),
            "spending_style": random.choice(["conservative", "moderate", "aggressive"]),
            "primary_category_1": random.choice(Category.objects.all()),
            "primary_category_2": random.choice(Category.objects.all()),
            "short_term_savings_goal": random.uniform(100, 500),
            "long_term_savings_goal": random.uniform(500, 2000),
            "income_range": random.choice(["low", "medium", "high"]),
            "saving_rate": random.uniform(5, 30),
        },
    )
    if not created:
        # UserPreferences가 이미 존재하면, 모든 필드를 업데이트합니다.
        obj.monthly_income = random.uniform(1000, 5000)
        obj.saving_goal = random.uniform(100, 1000)
        obj.spending_style = random.choice(["conservative", "moderate", "aggressive"])
        obj.primary_category_1 = random.choice(Category.objects.all())
        obj.primary_category_2 = random.choice(Category.objects.all())
        obj.short_term_savings_goal = random.uniform(100, 500)
        obj.long_term_savings_goal = random.uniform(500, 2000)
        obj.income_range = random.choice(["low", "medium", "high"])
        obj.saving_rate = random.uniform(5, 30)
        obj.save()  # 변경 사항을 데이터베이스에 저장합니다.


# 데이터 생성 완료 후 시간 측정
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Dummy data generation complete. It took {elapsed_time:.2f} seconds.")
