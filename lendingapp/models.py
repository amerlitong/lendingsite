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

	def name(self):
		return self.client_fk.name

	def payments(self):
		payment = Payment.objects.filter(credit_fk=self.id).aggregate(total=Sum(F('amount')))
		return payment['total'] if payment['total'] is not None else 0.0

	def __str__(self):
		return '{}, {}'.format(self.client_fk.name, str(self.amount))

	def delete(self,*args,**kwargs):
		ledger = Ledger.objects.filter(credit_id=self.id)
		ledger.delete()
		super(Credit,self).delete(*args,**kwargs)

	def save(self,*args, **kwargs):
		super(Credit,self).save(*args,**kwargs)
		ledger = Ledger()
		ledger.credit_id = self.id
		ledger.category = 'Credit'
		ledger.amount = self.amount
		ledger.interest = self.interest
		ledger.remarks = self.client_fk.name
		ledger.dt = self.dt
		ledger.save()

class Payment(CommonInfo):
	credit_fk = models.ForeignKey(Credit,verbose_name='Credit')

	def name(self):
		return self.credit_fk.client_fk.name

	def __str__(self):
		return '{}'.format(self.credit_fk.client_fk.name)

	def total(self):
		return self.amount + self.interest

	def delete(self,*args,**kwargs):
		ledger = Ledger.objects.filter(payment_id=self.id)
		ledger.delete()
		super(Payment,self).delete(*args,**kwargs)

	def save(self,*args, **kwargs):
		super(Payment,self).save(*args,**kwargs)
		ledger = Ledger()
		ledger.payment_id = self.id
		ledger.category = 'Payment'
		ledger.amount = self.amount + self.interest
		ledger.interest = self.interest
		ledger.remarks = self.credit_fk.client_fk.name
		ledger.dt = self.dt
		ledger.save()
		
class Ledger(CommonInfo):
	cats = [
		('Payment','Payment'),
		('Credit','Credit'),
		('Remit','Remit'),
		('Payment','Payment'),
		('Misc In','Misc In'),
		('Misc Out','Misc Out')
	]
	category = models.CharField(max_length=10,choices=cats)
	bank = models.CharField(max_length=10,choices=[('bdo','BDO'),('bpi','BPI')],blank=True)
	credit_id = models.IntegerField()
	payment_id = models.IntegerField()

	def save(self,*args, **kwargs):
		self.interest = 0.0
		super(Ledger,self).save(*args,**kwargs)