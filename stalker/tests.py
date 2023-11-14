from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, time


from .serializers import ExpenditureSerializer, UserPreferencesSerializer
from .models import Category, Expenditure, UserPreferences
from budget.models import UserBudget, BudgetCategory
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()


# model test
class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.name, "Test Category")


class ExpenditureModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Food")

    def test_expenditure_creation(self):
        expenditure = Expenditure.objects.create(
            user=self.user, category=self.category, amount=50.00, date=timezone.now()
        )
        self.assertEqual(expenditure.amount, 50.00)
        self.assertEqual(expenditure.user.username, "testuser")
        self.assertEqual(expenditure.category.name, "Food")


class UserPreferencesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category1 = Category.objects.create(name="Food")
        self.category2 = Category.objects.create(name="Utilities")

    def test_user_preferences_creation(self):
        preferences = UserPreferences.objects.create(
            user=self.user,
            monthly_income=1000.00,
            saving_goal=200.00,
            primary_category_1=self.category1,
            primary_category_2=self.category2,
        )
        self.assertEqual(preferences.monthly_income, 1000.00)
        self.assertEqual(preferences.saving_goal, 200.00)
        self.assertEqual(preferences.primary_category_1.name, "Food")
        self.assertEqual(preferences.primary_category_2.name, "Utilities")


# view test
class ExpenditureListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Food")
        Expenditure.objects.create(
            user=self.user, category=self.category, amount=100.00, date=timezone.now()
        )
        self.client.force_authenticate(user=self.user)

    def test_expenditure_list_retrieval(self):
        response = self.client.get("/api/v1/stalker/expenditures/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ExpenditureDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Food")
        self.expenditure = Expenditure.objects.create(
            user=self.user, category=self.category, amount=50.00, date=timezone.now()
        )
        self.client.force_authenticate(user=self.user)

    def test_expenditure_detail_retrieval(self):
        url = f"/api/v1/stalker/expenditures/{self.expenditure.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodaysExpenditureRecommendationViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.budget_category = BudgetCategory.objects.create(name="Budget Category")

        # 시간대를 고려한 시작 및 종료 날짜 생성
        start_of_month = timezone.make_aware(
            datetime.combine(timezone.now().date().replace(day=1), time.min)
        )
        end_of_month = timezone.make_aware(
            datetime.combine(timezone.now().date(), time.max)
        )

        self.user_budget = UserBudget.objects.create(
            user=self.user,
            category=self.budget_category,
            amount=1000.00,
            period_start=start_of_month,
            period_end=end_of_month,
        )

        # UserPreferences 인스턴스 생성
        UserPreferences.objects.create(
            user=self.user,
            monthly_income=5000.00,
            saving_goal=1000.00,
        )

        self.client.force_authenticate(user=self.user)

    def test_recommendation_view(self):
        response = self.client.get("/api/v1/stalker/expenditure/recommendation/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# serializer test
class ExpenditureSerializerTest(TestCase):
    def test_expenditure_serialization(self):
        user = User.objects.create_user(username="testuser", password="12345")
        category = Category.objects.create(name="Food")
        expenditure = Expenditure.objects.create(
            user=user, category=category, amount=100.00, date=timezone.now()
        )
        serializer = ExpenditureSerializer(expenditure)
        data = serializer.data
        self.assertEqual(data["amount"], "100.00")
        self.assertEqual(data["user"], user.id)


class UserPreferencesSerializerTest(TestCase):
    def test_user_preferences_serialization(self):
        user = User.objects.create_user(username="testuser", password="12345")
        category1 = Category.objects.create(name="Food")
        category2 = Category.objects.create(name="Utilities")
        preferences = UserPreferences.objects.create(
            user=user,
            monthly_income=1000.00,
            saving_goal=200.00,
            primary_category_1=category1,
            primary_category_2=category2,
        )
        serializer = UserPreferencesSerializer(preferences)
        data = serializer.data
        self.assertEqual(data["monthly_income"], "1000.00")
        self.assertEqual(data["saving_goal"], "200.00")
