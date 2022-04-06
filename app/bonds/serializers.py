from django.utils.translation import gettext as _
from django.conf import settings

from rest_framework import serializers, exceptions

from bonds import models
from bonds.signals import create_sell_transaction_signal
from bonds.utils.fetch_latest_exchange_rate import exchange_rate


class SellBondSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bond
        fields = ("id", "name", "number_of_bonds", "selling_price", "user")
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        bond = models.Bond.objects.create(
            user=self.context["request"].user,
            **validated_data
        )
        create_sell_transaction_signal.send(sender=models.Bond, bond=bond)

        return bond


class BondsListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=50, read_only=True)
    exchange_rate = exchange_rate()

    class Meta:
        model = models.Transaction
        fields = "__all__"

    def to_representation(self, data):
        currency = self.context.get("currency", None)
        currency_symbol = settings.DEFAULT_CURRENCY
        data = super().to_representation(data)
        bond = models.Bond.objects.get(id=data["bond"])
        selling_price = bond.selling_price
        if currency:
            if currency.lower() == 'usd':
                selling_price = float(selling_price) / float(self.exchange_rate)
                selling_price = "%.4f" % selling_price
                currency_symbol = "USD"

        return {
            "id": bond.id,
            "name": bond.name,
            "selling_price": f"{selling_price} {currency_symbol}",
            "status": data["status"],
            "number_of_bonds": bond.number_of_bonds
        }


class BuyBondsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = models.Bond
        fields = ("id", "name", "number_of_bonds", "selling_price")
        extra_kwargs = {
            "name": {"read_only": True},
            "number_of_bonds": {"read_only": True},
            "selling_price": {"read_only": True}
        }

    def create(self, validated_data):
        try:
            bond = models.Bond.objects.get(id=validated_data["id"])
            if bond.user == self.context["request"].user:
                raise exceptions.PermissionDenied(_("You can't buy your own bonds"))
            if models.Transaction.objects.filter(bond=bond, type=models.Transaction.TransactionType.BUY):
                raise exceptions.PermissionDenied(_("Operation is invalid"))
            models.Transaction.objects.create(
                bond=bond,
                type=models.Transaction.TransactionType.BUY,
                user=self.context["request"].user
            )
            return bond
        except models.Bond.DoesNotExist:
            raise exceptions.NotFound(_("Bond not found!"))
