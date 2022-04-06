from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.validators import MinLengthValidator, MaxValueValidator, \
    MinValueValidator

from core.models import UUIDBase


class Bond(UUIDBase):
    name = models.CharField(max_length=40, validators=[MinLengthValidator(3)])
    number_of_bonds = models.IntegerField(validators=[
            MaxValueValidator(10000),
            MinValueValidator(1)
        ]
    )
    selling_price = models.DecimalField(
        max_digits=13,
        decimal_places=4,
        validators=[
            MinValueValidator(0.0000),
            MaxValueValidator(100000000.0000)
        ]
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Transaction(UUIDBase):
    class TransactionType(models.TextChoices):
        SELL = ("sell", _("Sell"))
        BUY = ("buy", _("Buy"))

    type = models.CharField(max_length=4, choices=TransactionType.choices)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bond = models.ForeignKey(Bond, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.type} => {self.bond.name}"
