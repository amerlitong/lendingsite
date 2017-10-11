from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models, forms

def index(request):
	return render(request,'lendingapp/index.html')

@login_required
def client(request):
	clients = models.Client.objects.all()
	return render(request,'lendingapp/client.html',{'clients':clients})

def client_add(request):
	form = forms.ClientForm()
	if request.method == 'POST':
		form = forms.ClientForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Client added successfully!')
			return HttpResponseRedirect(reverse('client'))
		else:
			messages.warning(request,'Please check for all required field!')		
	return render(request,'lendingapp/client_form.html',{'form':form})

def client_edit(request,id):
	client = models.Client.objects.get(pk=id)
	form = forms.ClientForm(instance=client)
	if request.method == "POST":
		form = forms.ClientForm(instance=client, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('client'))	
	return render(request,'lendingapp/client_form.html',{'form':form})

def client_del(request,id):
	client = models.Client.objects.get(pk=id)
	credit = models.Credit.objects.filter(client_fk=client)
	if credit.count() == 0:
		client.delete()
	return HttpResponseRedirect(reverse('client'))

def credit(request,client_id):
	credits = models.Credit.objects.filter(client_fk=client_id)
	client = models.Client.objects.get(pk=client_id)
	return render(request,'lendingapp/credit.html',{'credits':credits,'client':client})

def credit_add(request,client_id):
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

def credit_edit(request,id):
	credit = models.Credit.objects.get(pk=id)
	client = credit.client_fk
	form = forms.CreditForm(instance=credit)
	if request.method == "POST":
		form = forms.CreditForm(instance=credit, data=request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.client_fk = client
			f.save()
			return HttpResponseRedirect(reverse('credit',args=(client.id,)))
	return render(request,'lendingapp/credit_form.html',{'form':form, 'client':client})

def credit_del(request,id):
	credit = models.Credit.objects.get(pk=id)
	payment = models.Payment.objects.filter(credit_fk=credit)
	if payment.count() == 0:
		credit.delete()
		return HttpResponseRedirect(reverse('credit',args=(credit.client_fk.id,)))
	return HttpResponseRedirect(reverse('credit',args=(credit.client_fk.id,)))

def payment(request,client_id):
	client = models.Client.objects.get(pk=client_id)
	payments = models.Payment.objects.filter(credit_fk__client_fk_id=client_id)
	return render(request,'lendingapp/payment.html',{'payments':payments,'client':client})

def payment_add(request,credit_id):
	credit = models.Credit.objects.get(pk=credit_id)
	balance = credit.amount - credit.payments()
	client = credit.client_fk
	form = forms.PaymentForm(initial={'interest':balance * credit.interest})
	if request.method == "POST":
		form = forms.PaymentForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.credit_fk = credit
			f.save()
			return HttpResponseRedirect(reverse('client'))
	return render(request, 'lendingapp/payment_form.html',{'form':form,'client':client,'balance':balance})

def payment_edit(request,id):
	pass

def payment_del(request,id):
	payment = models.Payment.objects.get(pk=id).delete()
	return HttpResponseRedirect(reverse('payment',args=(payment.credit_fk.client_fk.id)))

def ledger(request):
	ledgers = models.Ledger.objects.all()
	return render(request,'lendingapp/ledger.html',{'ledgers':ledgers})

def ledger_add(request):
	form = forms.LedgerForm()
	if request.method == "POST":
		form = forms.LedgerForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('ledger'))
	return render(request, 'lendingapp/ledger_form.html',{'form':form})

def ledger_edit(request,id):
	pass

def ledger_del(request,id):
	pass