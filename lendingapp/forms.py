from django.forms import ModelForm

from .models import Client, Credit, Payment, Ledger

class ClientForm(ModelForm):
	class Meta:
		model = Client
		fields = '__all__'

class CreditForm(ModelForm):
	class Meta:
		model = Credit
		fields = '__all__'

class PaymentForm(ModelForm):
	class Meta:
		model = Payment
		fields = '__all__'

class LedgerForm(ModelForm):
	class Meta:
		model = Ledger
		fields = '__all__'