from django.shortcuts import render
from . import models, forms

def index(request):
	return render(request,'lendingapp/index.html')

def client(request):
	clients = models.Client.objects.all()
	return render(request,'lendingapp/client.html',{'clients':clients})

def client_add(request):
	form = forms.ClientForm()
	if request.method == 'POST':
		form = forms.ClientForm(request.POST)
		if form.is_valid():
			pass
			
	return render(request,'lendingapp/client_form.html',{'form':form})

def credit(request,client_id):
	credits = models.Credit.objects.filter(client_fk=client_id)
	return render(request,'lendingapp/credit.html',{'credits':credits})

def credit_add(request, client_id):
	pass

def payment(request,client_id):
	payments = models.Payment.objects.filter(credit_fk__client_fk_id=client_id)
	return render(request,'lendingapp/payment.html',{'payments':payments})

def payment_add(request,credit_id):
	pass

def ledger(request):
	ledgers = models.Ledger.objects.all()
	return render(request,'lendingapp/ledger.html',{'ledgers':ledgers})

def ledger_add(request):
	pass