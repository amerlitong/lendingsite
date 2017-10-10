from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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
			form.save()
			return HttpResponseRedirect(reverse('client'))		
	return render(request,'lendingapp/client_form.html',{'form':form})

def client_edit(request, id):
	client = models.Client.objects.get(pk=id)
	form = forms.ClientForm(instance=client)
	if request.method == "POST":
		form = forms.ClientForm(instance=client, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('client'))	
	return render(request,'lendingapp/client_form.html',{'form':form})

def credit(request,client_id):
	credits = models.Credit.objects.filter(client_fk=client_id)
	client = models.Client.objects.get(pk=client_id)
	return render(request,'lendingapp/credit.html',{'credits':credits,'client':client})

def credit_add(request, client_id):
	form = forms.CreditForm()
	client = models.Client.objects.get(pk=client_id)
	if request.method == "POST":
		form = forms.CreditForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.client_fk = client
			f.save()
			return HttpResponseRedirect(reverse('client'))
	return render(request,'lendingapp/credit_form.html',{'form':form, 'client':client})

def payment(request,client_id):
	client = models.Client.objects.get(pk=client_id)
	payments = models.Payment.objects.filter(credit_fk__client_fk_id=client_id)
	return render(request,'lendingapp/payment.html',{'payments':payments,'client':client})

def payment_add(request,credit_id):
	form = forms.PaymentForm()
	credit = models.Credit.objects.get(pk=credit_id)
	client = credit.client_fk
	if request.method == "POST":
		form = forms.PaymentForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.credit_fk = credit
			f.save()
			return HttpResponseRedirect(reverse('client'))
	return render(request, 'lendingapp/payment_form.html',{'form':form,'client':client})

def ledger(request):
	ledgers = models.Ledger.objects.all()
	return render(request,'lendingapp/ledger.html',{'ledgers':ledgers})

def ledger_add(request):
	pass