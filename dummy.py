import os
import django
from faker import Faker
import random
from datetime import date  # timedelta (기간 설정시)

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
    BudgetCategory.objects.create(name=name)

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
    Category.objects.create(name=name)

# 사용자별 지출 기록
for user in User.objects.all():
    for _ in range(20):  # 각 사용자당 20개의 지출 기록
        Expenditure.objects.create(
            user=user,
            date=fake.date_time_this_month(),
            amount=random.uniform(10, 200),
            category=random.choice(Category.objects.all()),
            memo=fake.sentence(),
            exclude_from_total=fake.boolean(),
        )

# 사용자 선호도 설정
for user in User.objects.all():
    UserPreferences.objects.create(
        user=user,
        monthly_income=random.uniform(1000, 5000),
        saving_goal=random.uniform(100, 1000),
        spending_style=random.choice(["conservative", "moderate", "aggressive"]),
        primary_category_1=random.choice(Category.objects.all()),
        primary_category_2=random.choice(Category.objects.all()),
        short_term_savings_goal=random.uniform(100, 500),
        long_term_savings_goal=random.uniform(500, 2000),
        income_range=random.choice(["low", "medium", "high"]),
        saving_rate=random.uniform(5, 30),
    )

print("Dummy data generation complete.")
