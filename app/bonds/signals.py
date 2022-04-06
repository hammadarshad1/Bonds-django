from django import dispatch
from django.dispatch import receiver

from bonds import models

create_sell_transaction_signal = dispatch.Signal(providing_args=['bond'])


@receiver(create_sell_transaction_signal)
def create_sell_transaction(sender, bond, **kwargs):
    models.Transaction.objects.create(
        user=bond.user,
        bond=bond,
        type=models.Transaction.TransactionType.SELL
    )
