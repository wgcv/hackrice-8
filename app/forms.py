from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Transaction

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount', 'type_transaction', 'description' )

class SpecialTransactionForm(ModelForm):
    transaction_type = (
    ('IV', 'Invest'),
    ('LD', 'Long-Term Desposit'),
    ('LO', 'Loan'),
    )
    class Meta:
        model = Transaction
        fields = ('amount', 'type_transaction', 'description' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_transaction'].choices = self.transaction_type
