from django.db import models

class CommonInfo(models.Model):
	amount = models.FloatField()
	interest = models.FloatField()
	dt = models.DateField()
	remarks = models.TextField(blank=True)

	class Meta:
		abstract = True

class Client(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=50,blank=True)
	mobile = models.CharField(max_length=50,blank=True)
	remarks = models.TextField(null=False,blank=True)

class Credit(CommonInfo):
	clientfk = models.ForeignKey(Client,verbose_name='Client')

class Payment(CommonInfo):
	creditfk = models.ForeignKey(Credit,verbose_name='Credit')
	clientfk = models.ForeignKey(Client,verbose_name='Client')
		
class Ledger(CommonInfo):
	cats = [
		('Remit','Remit'),
		('Misc In','Misc In'),
		('Misc Out','Misc Out')
	]
	category = models.CharField(max_length=10,choices=cats)
	bank = models.CharField(max_length=10,choices=[('bdo','BDO'),('bpi','BPI')],blank=True)