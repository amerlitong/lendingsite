from django import forms
from datetime import date
from . import models

class BaseForm(forms.ModelForm):
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
		model = models.Client
		fields = '__all__'

class CreditForm(BaseForm):
	class Meta:
		model = models.Credit
		exclude = ['clientfk']
		widgets = {
			'dt':forms.DateInput(attrs={'type':'date','value':date.today()}),
		}

class PaymentForm(BaseForm):
	class Meta:
		model = models.Payment
		exclude = ['creditfk','clientfk']
		widgets = {
			'dt':forms.DateInput(attrs={'type':'date','value':date.today()}),
		}

class LedgerForm(BaseForm):
	class Meta:
		model = models.Ledger
		fields = ['amount','dt','remarks','category','bank']
		widgets = {
			'dt':forms.DateInput(attrs={'type':'date','value':date.today()}),
			'category': forms.Select(),
			'bank': forms.Select(),
		}

class SearchForm(forms.Form):
	name = forms.CharField(max_length=50,label="Name",required=True)