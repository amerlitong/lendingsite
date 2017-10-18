from django.db import models

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

class Credit(CommonInfo):
	client_fk = models.ForeignKey(Client,verbose_name='Client')

	def name(self):
		return self.client_fk.name

class Payment(CommonInfo):
	credit_fk = models.ForeignKey(Credit,verbose_name='Credit')
		
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