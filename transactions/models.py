from django.db import models
from accounts.models import Account


class Transaction(models.Model):
    class Type(models.TextChoices):
        TRANSFER = 'TRANSFER', 'Transfer'
        DEPOSIT = 'DEPOSIT', 'Deposit'
        WITHDRAW = 'WITHDRAW', 'Withdraw'

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    destination_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incoming_transactions', null=True, blank=True)
    type = models.CharField(max_length=16, choices=Type.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True, help_text="Description optionnelle de la transaction")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        if self.type == self.Type.TRANSFER and self.destination_account:
            return f"Transfert {self.amount}€ de {self.account} vers {self.destination_account}"
        return f"{self.type} {self.amount}€ sur {self.account}"
