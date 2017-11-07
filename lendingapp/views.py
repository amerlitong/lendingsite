from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import CharField, Value, Sum, Q, OuterRef, Subquery
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
	credits = models.Credit.objects.select_related('clientfk').annotate(cat=Value('Credit',output_field=CharField())).values('id','amount','dt','clientfk__name','cat')
	payments = models.Payment.objects.select_related('clientfk').annotate(cat=Value('Payment',output_field=CharField())).values('id','amount','dt','clientfk__name','cat')
	ledger = models.Ledger.objects.values('id','amount','dt','remarks','category')
	summary_list = ledger.union(credits,payments,all=True).order_by('-dt')
	summary = paginators(request,summary_list)
	credit_sum = credits.aggregate(Credit=Sum('amount'))
	payment_sum = payments.aggregate(Payment=Sum('amount'))
	ledger_in = ledger.filter(category='Misc In').aggregate(LedgerIn=Sum('amount'))
	ledger_out = ledger.filter(Q(category='Misc Out') | Q(category='Remit')).aggregate(LedgerOut=Sum('amount'))
	totals = [credit_sum,payment_sum,ledger_in,ledger_out]
	cash = (totals[1]['Payment']+totals[2]['LedgerIn']) - (totals[0]['Credit']+totals[3]['LedgerOut'])
	return render(request,'lendingapp/index.html',{'summary':summary['obj_list'],'page':int(summary['page']),'totals':totals, 'cash':cash})

##############CLIENT#########################
@login_required
def client(request):
	form = forms.SearchForm()
	credits = models.Credit.objects.filter(clientfk=OuterRef('pk')).values('clientfk')
	sum_credits = credits.annotate(credits=Sum('amount')).values('credits')
	if request.method == 'POST' and 'search' in request.POST:
		form = forms.SearchForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name'].strip()
			client_list = models.Client.objects.filter(name__icontains=name).annotate(credits=Subquery(sum_credits)).prefetch_related('payment_set').annotate(payments=Sum('payment__amount'))
		else:	
			client_list = models.Client.objects.annotate(credits=Subquery(sum_credits)).prefetch_related('payment_set').annotate(payments=Sum('payment__amount'))
	else:
		client_list = models.Client.objects.annotate(credits=Subquery(sum_credits)).prefetch_related('payment_set').annotate(payments=Sum('payment__amount'))
	clients = paginators(request,client_list)
	return render(request,'lendingapp/client.html',{'clients':clients['obj_list'],'page':int(clients['page']),'form':form})

@login_required
def client_add(request):
	form = forms.ClientForm()
	if request.method == 'POST':
		form = forms.ClientForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Client added successfully!')
			return HttpResponseRedirect(reverse('client'))	
	return JsonResponse({'html_form':render_to_string('lendingapp/client_form.html',{'form':form},)})

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
	credit = models.Credit.objects.filter(clientfk=client)
	if credit.count() == 0:
		client.delete()
		messages.success(request,'Client deleted successfully!')
	else:
		messages.warning(request,'Cannot be deleted, Credits(s) available!')	
	return HttpResponseRedirect(reverse('client'))

##############CREDIT#########################
@login_required
def credit(request,client_id):
	credit_list = get_list_or_404(models.Credit.objects.filter(clientfk=client_id).prefetch_related('payment_set').annotate(payments=Sum('payment__amount')))
	credits = paginators(request,credit_list)
	return render(request,'lendingapp/credit.html',{'credits':credits['obj_list'],'client':credit_list[0].clientfk.name,'page':int(credits['page'])})

@login_required
def credit_add(request,client_id):
	client = get_object_or_404(models.Client,pk=client_id)
	form = forms.CreditForm()
	if request.method == "POST":
		form = forms.CreditForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.clientfk = client
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
			f.clientfk = credit.clientfk
			f.save()
			return HttpResponseRedirect(reverse('credit',args=(credit.clientfk.id,)))
	return render(request,'lendingapp/credit_form.html',{'form':form, 'client':credit.clientfk.name})

@login_required
def credit_del(request,id):
	credit = get_object_or_404(models.Credit,pk=id)
	payment = models.Payment.objects.filter(creditfk=credit)
	if payment.count() == 0:
		credit.delete()
		messages.success(request,'Credit deleted successfully!')
		return HttpResponseRedirect(reverse('credit',args=(credit.clientfk.id,)))
	else:
		messages.warning(request,'Cannot be deleted, Payment(s) available!')
		return HttpResponseRedirect(reverse('credit',args=(credit.clientfk.id,)))	
	return HttpResponseRedirect(reverse('credit',args=(credit.clientfk.id,)))

##############PAYMENT#########################
@login_required
def payment(request,client_id):
	payment_list = get_list_or_404(models.Payment.objects.filter(clientfk=client_id))
	payments = paginators(request,payment_list)
	return render(request,'lendingapp/payment.html',{'payments':payments['obj_list'],'client':payment_list[0].clientfk.name,'page':int(payments['page'])})

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
			f.creditfk = credit
			f.clientfk = credit.clientfk
			f.save()
			return HttpResponseRedirect(reverse('client'))
	return render(request, 'lendingapp/payment_form.html',{'form':form,'client':credit.clientfk.name,'balance':balance})

@login_required
def payment_edit(request,id):
	payment = get_object_or_404(models.Payment,pk=id)
	balance = payment.creditfk.amount - payment.amount
	form = forms.PaymentForm(instance=payment)
	if request.method == "POST":
		form = forms.PaymentForm(instance=payment, data=request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.creditfk = payment.creditfk
			f.clientfk = payment.clientfk
			f.save()
			return HttpResponseRedirect(reverse('payment',args=(payment.clientfk.id,)))
	return render(request, 'lendingapp/payment_form.html',{'form':form,'client':payment.clientfk.name,'balance':balance})

@login_required
def payment_del(request,id):
	payment = get_object_or_404(models.Payment,pk=id)
	payment.delete()
	return HttpResponseRedirect(reverse('payment',args=(payment.clientfk.id,)))

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