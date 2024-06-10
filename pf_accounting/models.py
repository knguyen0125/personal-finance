from django.core.exceptions import ValidationError
from django.db import models, transaction as db_transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Journal(models.Model):
    """
    Journal model
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=65535)

    def __str__(self):
        return self.name


class Account(models.Model):
    """
    Account model
    """

    ACCOUNT_TYPE = (
        ("asset", _("Asset")),
        ("liability", _("Liability")),
        ("income", _("Income")),
        ("expense", _("Expense")),
        ("equity", _("Equity")),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=65535)

    type = models.CharField(max_length=255, choices=ACCOUNT_TYPE)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Transaction model
    """

    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    date = models.DateTimeField()

    description = models.CharField(max_length=65535)

    def __str__(self):
        return self.description

    @db_transaction.atomic
    def save_with_entries(self, entries_data):
        total_amount = sum(entry["amount"] for entry in entries_data)

        if total_amount != 0:
            raise ValidationError(
                _("The sum of all related Entry amounts must be zero.")
            )

        self.save()

        # Remove all existing entries
        self.entry_set.all().delete()

        # Create new entries
        for entry_data in entries_data:
            Entry.objects.create(transaction=self, **entry_data)


class Entry(models.Model):
    """
    Entry model
    """

    amount = models.DecimalField(max_digits=19, decimal_places=4)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
