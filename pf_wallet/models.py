from django.db import models
from django.conf import settings


class Account(models.Model):
    """
    Account model

    Account is a place to record transactions that occur.
    """

    pass


# Create your models here.
class Wallet(models.Model):
    """
    Wallet model

    In accounting terms, this is roughly equivalent to an "account"
    """

    WALLET_TYPE = (
        ("cash", "Cash"),
        ("checking", "Checking"),
        ("savings", "Savings"),
        ("credit_card", "Credit Card"),
    )

    name = models.CharField(max_length=65535)

    wallet_type = models.CharField(max_length=255, choices=WALLET_TYPE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Transaction(models.Model):
    """
    Transaction model
    """

    date = models.DateField()

    amount = models.DecimalField(max_digits=19, decimal_places=4)

    description = models.CharField(max_length=65535)

    accounts = models.ManyToManyField(Account)
