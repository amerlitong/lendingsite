from django.db import models
from django.db.models import Sum, F

class CommonInfo(models.Model):
	amount = models.FloatField()
	interest = models.FloatField()
	dt = models.DateField(verbose_name='date')
	remarks = models.TextField(blank=True)

class Client(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=50,blank=True)
	mobile = models.CharField(max_length=50,blank=True)
	remarks = models.TextField(null=False,blank=True)

	def __str__(self):
		return self.name

	def credits(self):
		credit = Credit.objects.filter(client_fk=self.id).aggregate(Sum('amount'))
		return credit['amount__sum'] if credit['amount__sum'] is not None else 0.0

	def payments(self):
		payment = Payment.objects.filter(credit_fk__client_fk=self.id).aggregate(total=Sum(F('amount')))
		return payment['total'] if payment['total'] is not None else 0.0

class Credit(CommonInfo):
	client_fk = models.ForeignKey(Client,verbose_name='Client')

	def cat(self):
		return 'Credit'

	def name(self):
		return self.client_fk.name

	def payments(self):
		payment = Payment.objects.filter(credit_fk=self.id).aggregate(total=Sum(F('amount')))
		return payment['total'] if payment['total'] is not None else 0.0

	def __str__(self):
		return '{}, {}'.format(self.client_fk.name, 'Credit')

class Payment(CommonInfo):
	credit_fk = models.ForeignKey(Credit,verbose_name='Credit')

	def name(self):
		return self.credit_fk.client_fk.name

	def __str__(self):
		return '{}, {}'.format(self.credit_fk.client_fk.name, 'Payment')

	def total(self):
		return self.amount + self.interest
		
class Ledger(CommonInfo):
	cats = [
		('Remit','Remit'),
		('Misc In','Misc In'),
		('Misc Out','Misc Out')
	]
	category = models.CharField(max_length=10,choices=cats)
	bank = models.CharField(max_length=10,choices=[('bdo','BDO'),('bpi','BPI')],blank=True)
	credit_id = models.IntegerField(null=True)
	payment_id = models.IntegerField()

	def save(self,*args, **kwargs):
		self.interest = 0.0
		super(Ledger,self).save(*args,**kwargs)