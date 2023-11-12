from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expenditure
from .serializers import ExpenditureSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from django.utils.dateparse import parse_datetime


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
