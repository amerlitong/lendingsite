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

	def balance(self):
		credit = self.credits()
		payment = self.payments()
		if payment == 0.0:
			return credit
		else:
			return credit - payment

class Credit(CommonInfo):
	client_fk = models.ForeignKey(Client,verbose_name='Client')

	def name(self):
		return self.client_fk.name

	def payments(self):
		payment = Payment.objects.filter(credit_fk=self.id).aggregate(total=Sum(F('amount')))
		return payment['total']

	def __str__(self):
		return '{}, {}'.format(self.client_fk.name, str(self.amount))

	def save(self,*args, **kwargs):
		ledger = Ledger()
		ledger.category = 'cre'
		ledger.amount = self.amount
		ledger.interest = 0.0
		ledger.remarks = self.client_fk.name
		ledger.dt = self.dt
		ledger.save()
		super(Credit,self).save(*args,**kwargs)

class Payment(CommonInfo):
	credit_fk = models.ForeignKey(Credit,verbose_name='Credit')

	def name(self):
		return self.credit_fk.client_fk.name

	def __str__(self):
		return '{}'.format(self.credit_fk.client_fk.name)

	def total(self):
		return self.amount + self.interest

	def save(self,*args, **kwargs):
		ledger = Ledger()
		ledger.category = 'pay'
		ledger.amount = self.amount + self.interest
		ledger.interest = 0.0
		ledger.remarks = self.credit_fk.client_fk.name
		ledger.dt = self.dt
		ledger.save()
		super(Payment,self).save(*args,**kwargs)

class Ledger(CommonInfo):
	cats = [
		('pay','Payment'),
		('cre','Credit'),
		('rem','Remit'),
		('pay','Payment'),
		('min','Misc In'),
		('mout','Misc Out')
	]
	category = models.CharField(max_length=10,choices=cats)
	bank = models.CharField(max_length=10,choices=[('bdo','BDO'),('bpi','BPI')],blank=True)