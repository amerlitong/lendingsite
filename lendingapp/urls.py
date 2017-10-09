from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^client/', views.client, name='client'),
	url(r'^client/add/', views.client, name='client_add'),
	url(r'^client/edit/(?P<id>[0-9]+)', views.client, name='client_edit'),
	url(r'^credit/(?P<client_id>[0-9]+)', views.credit, name='credit'),
	url(r'^credit/add/(?P<client_id>[0-9]+)', views.credit, name='credit_add'),
	url(r'^credit/edit/(?P<id>[0-9]+)', views.credit, name='credit_edit'),
	url(r'^payment/(?P<client_id>[0-9]+)', views.payment, name='payment'),
	url(r'^payment/add/(?P<client_id>[0-9]+)/(?P<credit_id>[0-9]+)', views.payment, name='payment_add'),
	url(r'^payment/edit/(?P<id>[0-9]+)', views.payment, name='payment_edit'),
	url(r'^ledger/', views.ledger, name='ledger'),
	url(r'^ledger/add', views.ledger, name='ledger_add'),
	url(r'^ledger/edit/(?P<id>[0-9]+)', views.ledger, name='ledger_edit'),
]