from django.shortcuts import render
from .models import Client, Credit, Payment, Ledger

def index(request):
	return render(request,'index.html')

def client(request):
	clients = Client.objects.all()
	return render(request,'client.html',{'clients':clients})

def credit(request,client_id):
	credits = Credit.objects.filter(client_fk=client_id)
	return render(request,'credit.html',{'credits':credits})

def payment(request):
	payments = Payment.objects.all()
	return render(request,'client.html',{'payments':payments})

def ledger(request):
	ledger = Ledger.objects.all()
	return render(request,'client.html',{'ledger':ledger})
