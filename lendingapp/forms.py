from django.forms import ModelForm

from .models import Client, Credit, Payment, Ledger

class ClientForm(ModelForm):
	class Meta:
		model = Client
		fields = '__all__'

class CreditForm(ModelForm):
	class Meta:
		model = Credit
		exclude = ['client_fk']

class PaymentForm(ModelForm):
	class Meta:
		model = Payment
		exclude = ['credit_fk']

class LedgerForm(ModelForm):
	class Meta:
		model = Ledger
		fields = '__all__'