from django.db.models import Case, When, CharField, Value

from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from bonds import models
from bonds.serializers import SellBondSerializer, BondsListSerializer, \
    BuyBondsSerializer


class SellBondViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SellBondSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListBondsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BondsListSerializer
    permission_classes = (permissions.IsAuthenticated, )
    currency_param_config = openapi.Parameter(
            'currency',
            in_=openapi.IN_QUERY,
            description='currency',
            type=openapi.TYPE_STRING
        )

    def get_queryset(self):
        queryset = (
            models.Transaction.objects.all()
            .annotate(status=Case(
                When(type=models.Transaction.TransactionType.BUY, then=Value("Purchased")),
                When(type=models.Transaction.TransactionType.SELL, then=Value("Up for Sell")),
                output_field=CharField()
            )).order_by("bond", "status").distinct("bond")
        )

        return queryset

    @swagger_auto_schema(manual_parameters=[currency_param_config])
    def list(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True,
            context={"currency": request.GET.get("currency", None)}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class BondBuyViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = BuyBondsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
