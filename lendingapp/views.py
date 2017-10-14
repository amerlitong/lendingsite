from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models, forms

page_count = 10

def error_404(request):
	return render(request,'lendingapp/404.html',{})

##############INDEX#########################
@login_required
def index(request):
	credits = models.Credit.objects.values('amount','interest','dt','client_fk','client_fk')
	payments = models.Payment.objects.values('amount','interest','dt','credit_fk__client_fk','credit_fk__client_fk')
	ledger = models.Ledger.objects.values('amount','interest','dt','category','remarks')
	summary = ledger.union(credits,payments,all=True)
	return render(request,'lendingapp/index.html',{'summary':summary})

##############CLIENT#########################
@login_required
def client(request):
	client_list = models.Client.objects.all()
	paginator = Paginator(client_list,page_count)
	page = request.GET.get('page')

	try:
		clients = paginator.page(page)
	except PageNotAnInteger:
		clients = paginator.page(1)
		page = 1
	except EmptyPage:
		clients = paginator.page(paginator.num_pages)

	return render(request,'lendingapp/client.html',{'clients':clients,'page':int(page)})
@login_required
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

@login_required
def client_edit(request,id):
	client = get_object_or_404(models.Client,pk=id)
	form = forms.ClientForm(instance=client)
	if request.method == "POST":
		form = forms.ClientForm(instance=client, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('client'))	
	return render(request,'lendingapp/client_form.html',{'form':form})

@login_required
def client_del(request,id):
	client = get_object_or_404(models.Client,pk=id)
	credit = models.Credit.objects.filter(client_fk=client)
	if credit.count() == 0:
		client.delete()
	return HttpResponseRedirect(reverse('client'))

##############CREDIT#########################
@login_required
def credit(request,client_id):
	client = get_object_or_404(models.Client,pk=client_id)
	credits_list = models.Credit.objects.filter(client_fk=client_id)
	paginator = Paginator(credits_list,page_count)
	page = request.GET.get('page')
	
	try:
		credits = paginator.page(page)
	except PageNotAnInteger:
		credits = paginator.page(1)
		page = 1
	except EmptyPage:
		credits = paginator.page(paginator.num_pages)

	return render(request,'lendingapp/credit.html',{'credits':credits,'client':client,'page':int(page)})

@login_required
def credit_add(request,client_id):
	client = get_object_or_404(models.Client,pk=client_id)
	form = forms.CreditForm()
	if request.method == "POST":
		form = forms.CreditForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.client_fk = client
			f.save()
			return HttpResponseRedirect(reverse('client'))
	return render(request,'lendingapp/credit_form.html',{'form':form, 'client':client})

@login_required
def credit_edit(request,id):
	credit = get_object_or_404(models.Credit, pk=id)
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

@login_required
def credit_del(request,id):
	credit = get_object_or_404(models.Credit,pk=id)
	payment = models.Payment.objects.filter(credit_fk=credit)
	if payment.count() == 0:
		credit.delete()
		messages.success(request,'Credit deleted successfully!')
		return HttpResponseRedirect(reverse('credit',args=(credit.client_fk.id,)))
	else:
		messages.warning(request,'Cannot be deleted, Payment(s) available!')
		return HttpResponseRedirect(reverse('credit',args=(credit.client_fk.id,)))	
	return HttpResponseRedirect(reverse('credit',args=(credit.client_fk.id,)))

##############PAYMENT#########################
@login_required
def payment(request,client_id):
	client = get_object_or_404(models.Client,pk=client_id)
	payments_list = models.Payment.objects.filter(credit_fk__client_fk_id=client_id)
	paginator = Paginator(payments_list,page_count)
	page = request.GET.get('page')
	
	try:
		payments = paginator.page(page)
	except PageNotAnInteger:
		payments = paginator.page(1)
		page = 1
	except EmptyPage:
		payments = paginator.page(paginator.num_pages)

	return render(request,'lendingapp/payment.html',{'payments':payments,'client':client,'page':int(page)})

@login_required
def payment_add(request,credit_id):
	credit = get_object_or_404(models.Credit,pk=credit_id)
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

@login_required
def payment_edit(request,id):
	payment = get_object_or_404(models.Payment.objects.get,pk=id)
	credit = payment.credit_fk
	client = credit.client_fk
	balance = credit.amount - payment.amount
	form = forms.PaymentForm(instance=payment)
	if request.method == "POST":
		form = forms.PaymentForm(instance=payment, data=request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.credit_fk = credit
			f.save()
			return HttpResponseRedirect(reverse('payment',args=(credit.client_fk.id)))
	return render(request, 'lendingapp/payment_form.html',{'form':form,'client':client,'balance':balance})

@login_required
def payment_del(request,id):
	payment = models.Payment.objects.get(pk=id).delete()
	return HttpResponseRedirect(reverse('payment',args=(payment.credit_fk.client_fk.id)))

##############LEDGER#########################
@login_required
def ledger(request):
	ledgers_list = models.Ledger.objects.all()
	paginator = Paginator(ledgers_list,page_count)
	page = request.GET.get('page')
	
	try:
		ledgers = paginator.page(page)
	except PageNotAnInteger:
		ledgers = paginator.page(1)
		page = 1
	except EmptyPage:
		ledgers = paginator.page(paginator.num_pages)
	return render(request,'lendingapp/ledger.html',{'ledgers':ledgers,'page':int(page)})

@login_required
def ledger_add(request):
	form = forms.LedgerForm(initial={'category':'Misc Out'})
	if request.method == "POST":
		form = forms.LedgerForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Ledger successfully added!')
			return HttpResponseRedirect(reverse('ledger'))
	return render(request, 'lendingapp/ledger_form.html',{'form':form})

@login_required
def ledger_edit(request,id):
	ledger = get_object_or_404(models.Ledger,pk=id)
	form = forms.LedgerForm(instance=ledger)
	if request.method == "POST":
		form = forms.LedgerForm(instance=ledger, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Ledger successfully edited!')
			return HttpResponseRedirect(reverse('ledger'))
	return render(request, 'lendingapp/ledger_form.html',{'form':form})

@login_required
def ledger_del(request,id):
	ledger = get_object_or_404(models.Ledger,pk=id)
	if ledger.category not in ['Payment','Credit']:
		ledger.delete()
		messages.success(request,'Ledger successfully deleted!')
		return HttpResponseRedirect(reverse('ledger'))
	else:
		messages.warning(request,'Ledger deletion failed!')
	return HttpResponseRedirect(reverse('ledger'))