from django.test import TestCase
from django.contrib.auth.models import User
from .models import BudgetCategory, UserBudget
from datetime import date


class BudgetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트용 사용자 생성
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()

        # 테스트용 예산 카테고리 생성
        test_category = BudgetCategory.objects.create(
            name="Test Category", description="Test Description"
        )
        test_category.save()

        # 테스트용 사용자 예산 생성
        UserBudget.objects.create(
            category=test_category,
            amount=1000.00,
            period_start=date.today(),
            period_end=date.today(),
            user=test_user,
        )

    def test_budget_category_creation(self):
        category = BudgetCategory.objects.get(id=1)
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test Description")

    def test_user_budget_creation(self):
        user_budget = UserBudget.objects.get(id=1)
        self.assertEqual(user_budget.amount, 1000.00)
        self.assertEqual(user_budget.category.name, "Test Category")
        self.assertEqual(user_budget.user.username, "testuser")

    def test_total_user_budget_for_period(self):
        user = User.objects.get(username="testuser")
        total_budget = UserBudget.get_total_user_budget_for_period(
            user, date.today(), date.today()
        )
        self.assertEqual(total_budget, 1000.00)
