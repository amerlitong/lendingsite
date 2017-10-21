from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import CharField, Value, Sum, Q
from . import models, forms

page_count = 10

def error_404(request):
	return render(request,'lendingapp/404.html',{})

def paginators(request,obj):
	paginator = Paginator(obj,page_count)
	page = request.GET.get('page')

	try:
		obj_list = paginator.page(page)
	except PageNotAnInteger:
		obj_list = paginator.page(1)
		page = 1
	except EmptyPage:
		obj_list = paginator.page(paginator.num_pages)

	return {'obj_list':obj_list,'page':page}

##############INDEX#########################
@login_required
def index(request):
	clients = models.Client.objects.prefetch_related('credit_set__payment_set')
	credits = clients.filter(credit__id__isnull=False).annotate(cat=Value('Credit',output_field=CharField())).values('credit__id','credit__amount','credit__interest','credit__dt','name','cat')
	payments = clients.filter(credit__payment__id__isnull=False).annotate(cat=Value('Payment',output_field=CharField()))
	payments = payments.values('credit__payment__id','credit__payment__amount','credit__payment__interest','credit__payment__dt','name','cat')
	ledger = models.Ledger.objects.values('id','amount','interest','dt','remarks','category')
	summary_list = ledger.union(credits,payments,all=True).order_by('-dt')
	summary = paginators(request,summary_list)
	credit_sum = credits.aggregate(Credit=Sum('credit__amount'))
	payment_sum = payments.aggregate(Payment=Sum('credit__payment__amount'))
	ledger_in = ledger.filter(category='Misc In').aggregate(LedgerIn=Sum('amount'))
	ledger_out = ledger.filter(Q(category='Misc Out') | Q(category='Remit')).aggregate(LedgerIn=Sum('amount'))
	totals = [credit_sum,payment_sum,ledger_in,ledger_out]
	return render(request,'lendingapp/index.html',{'summary':summary['obj_list'],'page':int(summary['page']),'totals':totals})

##############CLIENT#########################
@login_required
def client(request):
	client_list = models.Client.objects.prefetch_related().annotate(credits=Sum('credit__amount')).values('id').annotate(payments=Sum('credit__payment__amount'))
	clients = paginators(request,client_list)
	return render(request,'lendingapp/client.html',{'clients':clients['obj_list'],'page':int(clients['page'])})

@login_required
def client_add(request):
	form = forms.ClientForm()
	if request.method == 'POST':
		form = forms.ClientForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Client added successfully!')
			return HttpResponseRedirect(reverse('client'))	
	return render(request,'lendingapp/client_form.html',{'form':form})

@login_required
def client_edit(request,id):
	client = get_object_or_404(models.Client,pk=id)
	form = forms.ClientForm(instance=client)
	if request.method == "POST":
		form = forms.ClientForm(instance=client, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Client edited successfully!')
			return HttpResponseRedirect(reverse('client'))	
	return render(request,'lendingapp/client_form.html',{'form':form})

@login_required
def client_del(request,id):
	client = get_object_or_404(models.Client,pk=id)
	credit = models.Credit.objects.filter(client_fk=client)
	if credit.count() == 0:
		client.delete()
		messages.success(request,'Client deleted successfully!')
	else:
		messages.warning(request,'Cannot be deleted, Credits(s) available!')	
	return HttpResponseRedirect(reverse('client'))

##############CREDIT#########################
@login_required
def credit(request,client_id):
	credit_list = get_list_or_404(models.Credit.objects.filter(client_fk_id=client_id).prefetch_related('payment_set').annotate(payments=Sum('payment__amount')))
	credits = paginators(request,credit_list)
	return render(request,'lendingapp/credit.html',{'credits':credits['obj_list'],'client':credit_list[0].client_fk.name,'page':int(credits['page'])})

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
			messages.success(request,'Client added successfully!')
			return HttpResponseRedirect(reverse('client'))
	return render(request,'lendingapp/credit_form.html',{'form':form, 'client':client.name})

@login_required
def credit_edit(request,id):
	credit = get_object_or_404(models.Credit, pk=id)
	form = forms.CreditForm(instance=credit)
	if request.method == "POST":
		form = forms.CreditForm(instance=credit, data=request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.client_fk = credit.client_fk
			f.save()
			return HttpResponseRedirect(reverse('credit',args=(credit.client_fk.id,)))
	return render(request,'lendingapp/credit_form.html',{'form':form, 'client':credit.client_fk.name})

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
	payment_list = models.Payment.objects.select_related('credit_fk__client_fk').filter(credit_fk__client_fk_id=client_id)
	payments = paginators(request,payment_list)
	return render(request,'lendingapp/payment.html',{'payments':payments['obj_list'],'client':payment_list[0].credit_fk.client_fk.name,'page':int(payments['page'])})

@login_required
def payment_add(request,credit_id):
	credit = get_object_or_404(models.Credit.objects.prefetch_related('payment_set').annotate(payments=Sum('payment__amount')),pk=credit_id)
	if credit.payments:
		balance = credit.amount - credit.payments
	else:
		balance = credit.amount	
	form = forms.PaymentForm(initial={'interest':balance * credit.interest})
	if request.method == "POST":
		form = forms.PaymentForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.credit_fk = credit
			f.save()
			return HttpResponseRedirect(reverse('client'))
	return render(request, 'lendingapp/payment_form.html',{'form':form,'client':credit.client_fk.name,'balance':balance})

@login_required
def payment_edit(request,id):
	payment = get_object_or_404(models.Payment,pk=id)
	balance = payment.credit_fk.amount - payment.amount
	form = forms.PaymentForm(instance=payment)
	if request.method == "POST":
		form = forms.PaymentForm(instance=payment, data=request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.credit_fk = payment.credit_fk
			f.save()
			return HttpResponseRedirect(reverse('payment',args=(payment.credit_fk.client_fk.id,)))
	return render(request, 'lendingapp/payment_form.html',{'form':form,'client':payment.credit_fk.client_fk.name,'balance':balance})

@login_required
def payment_del(request,id):
	payment = get_object_or_404(models.Payment,pk=id)
	payment.delete()
	return HttpResponseRedirect(reverse('payment',args=(payment.credit_fk.client_fk.id,)))

##############LEDGER#########################
@login_required
def ledger_add(request):
	form = forms.LedgerForm(initial={'category':'Misc Out'})
	if request.method == "POST":
		form = forms.LedgerForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Ledger successfully added!')
			return HttpResponseRedirect(reverse('index'))
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
			return HttpResponseRedirect(reverse('index'))
	return render(request, 'lendingapp/ledger_form.html',{'form':form})

@login_required
def ledger_del(request,id):
	ledger = get_object_or_404(models.Ledger,pk=id)
	ledger.delete()
	messages.success(request,'Ledger successfully deleted!')
	return HttpResponseRedirect(reverse('index'))