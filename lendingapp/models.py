from django.db import models

class Client(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=50,blank=True)
	mobile = models.CharField(max_length=50,blank=True)
	remarks = models.TextField(null=False,blank=True)

class Credit(models.Model):
	amount = models.FloatField()
	interest = models.FloatField()
	dt = models.DateField(verbose_name='date')
	remarks = models.TextField(blank=True)
	clientfk = models.ForeignKey(Client,verbose_name='Client')

class Payment(models.Model):
	amount = models.FloatField()
	interest = models.FloatField()
	dt = models.DateField(verbose_name='date')
	remarks = models.TextField(blank=True)
	creditfk = models.ForeignKey(Credit,verbose_name='Credit')
	clientfk = models.ForeignKey(Client,verbose_name='Client')
		
class Ledger(models.Model):
	amount = models.FloatField()
	dt = models.DateField(verbose_name='date')
	remarks = models.TextField(blank=True)
	cats = [
		('Remit','Remit'),
		('Misc In','Misc In'),
		('Misc Out','Misc Out')
	]
	category = models.CharField(max_length=10,choices=cats)
	bank = models.CharField(max_length=10,choices=[('bdo','BDO'),('bpi','BPI')],blank=True)