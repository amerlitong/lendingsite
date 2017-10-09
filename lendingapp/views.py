from django.shortcuts import render
from .models import Client, Credit, Payment, Ledger

def index(request):
	return render(request,'lendingapp/index.html')

def client(request):
	clients = Client.objects.all()
	return render(request,'lendingapp/client.html',{'clients':clients})

def credit(request,client_id):
	credits = Credit.objects.filter(client_fk=client_id)
	return render(request,'lendingapp/credit.html',{'credits':credits})

def payment(request,client_id):
	payments = Payment.objects.filter(credit_fk__client_fk_id=client_id)
	return render(request,'lendingapp/payment.html',{'payments':payments})

def ledger(request):
	ledgers = Ledger.objects.all()
	return render(request,'lendingapp/ledger.html',{'ledgers':ledgers})