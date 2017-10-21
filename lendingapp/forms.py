from django.forms import ModelForm, Select, DateInput
from datetime import date
from .models import Client, Credit, Payment, Ledger

class BaseForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(BaseForm,self).__init__(*args,**kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update(
				{
					'class':'form-control',
					'placeholder': field.upper()
				}
			)
	def as_p(self):
		return self._html_output(
            normal_row = '<p%(html_class_attr)s></p> <p>%(field)s%(help_text)s</p>',
            error_row = '%s',
            row_ender = '</p>',
            help_text_html = ' <span class="helptext">%s</span>',
            errors_on_separate_row = True)

class ClientForm(BaseForm):
	class Meta:
		model = Client
		fields = '__all__'

class CreditForm(BaseForm):
	class Meta:
		model = Credit
		exclude = ['clientfk']
		widgets = {
			'dt':DateInput(attrs={'type':'date','value':date.today()}),
		}

class PaymentForm(BaseForm):
	class Meta:
		model = Payment
		exclude = ['creditfk','clientfk']
		widgets = {
			'dt':DateInput(attrs={'type':'date','value':date.today()}),
		}

class LedgerForm(BaseForm):
	class Meta:
		model = Ledger
		fields = ['amount','dt','remarks','category','bank']
		widgets = {
			'dt':DateInput(attrs={'type':'date','value':date.today()}),
			'category': Select(),
			'bank': Select(),
		}
