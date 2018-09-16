from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DataUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.IntegerField(default = 0)
    next_progress = models.IntegerField(default = 80)
    level = models.IntegerField(default = 1)
    amount = models.DecimalField(max_digits=30, decimal_places=2, default = 0)
    def __str__(self):
        return self.user.username
transaction_type = (
    ('DP', 'Deposit'),
    ('WD', 'Withdrawal'),
    ('PM', 'Payment'),
    ('TR', 'Transference'),
    ('IV', 'Invest'),
    ('LD', 'Long-Term Desposit'),
    ('LO', 'Loan'),

)
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    type_transaction = models.CharField(max_length=2, choices=transaction_type)
    description = models.CharField(max_length=250, blank=True)

class MessageDescription(models.Model):
    tittle = models.CharField(max_length=75, blank=True)
    short_description = models.CharField(max_length=500, blank=True)
    description = models.TextField(max_length=5000, blank=True)
    def __str__(self):
        return self.tittle

class Message(models.Model):
    message = models.ForeignKey(MessageDescription, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

