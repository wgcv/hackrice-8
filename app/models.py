from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DataUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.IntegerField(default = 0)
    level = models.IntegerField(default = 1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0)

transaction_type = (
    ('DP', 'Deposit'),
    ('WD', 'Withdrawal'),
    ('PM', 'Payment'),
    ('TR', 'Transference'),
)
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    type_transaction = models.CharField(max_length=2, choices=transaction_type)
    description = models.CharField(max_length=250, blank=True)