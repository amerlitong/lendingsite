import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Client,Credit,Payment,Ledger

def export_actions(modeladmin,request,queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="export.csv"'
	writer = csv.writer(response)
	writer.writerow(['ID','NAME','ADDRESS','MOBILE','REMARKS'])
	qset = queryset.values_list('id','name','address','mobile','remarks')
	for qs in qset:
		writer.writerow(qs)
	return response

export_actions.short_description = 'Export to CSV'

class ClientAdmin(admin.ModelAdmin):
	list_display = ['name','address','mobile','credits','payments','remarks']
	search_fields = ['name']
	list_per_page = 20
	ordering = ['name']
	actions = [export_actions]

class CreditAdmin(admin.ModelAdmin):
	list_display = ['name','amount','interest','dt','payments','remarks']
	search_fields = ['client_fk__name']

class PaymentAdmin(admin.ModelAdmin):
	list_display = ['name','amount','interest','total','dt','remarks']
	search_fields = ['credit_fk__client_fk__name']

class LedgerAdmin(admin.ModelAdmin):
	list_display = ['amount','dt','remarks','category','bank']
	search_fields = ['remarks']
	list_filter = ['category','bank']

admin.site.register(Client, ClientAdmin)
admin.site.register(Credit, CreditAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Ledger, LedgerAdmin)