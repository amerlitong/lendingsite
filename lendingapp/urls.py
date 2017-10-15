from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^client/add/$', views.client_add, name='client_add'),
	url(r'^client/edit/(?P<id>[0-9]+)/$', views.client_edit, name='client_edit'),
	url(r'^client/del/(?P<id>[0-9]+)/$', views.client_del, name='client_del'),
	url(r'^client/$', views.client, name='client'),
	url(r'^credit/(?P<client_id>[0-9]+)/$', views.credit, name='credit'),
	url(r'^credit/add/(?P<client_id>[0-9]+)/$', views.credit_add, name='credit_add'),
	url(r'^credit/edit/(?P<id>[0-9]+)/$', views.credit_edit, name='credit_edit'),
	url(r'^credit/del/(?P<id>[0-9]+)/$', views.credit_del, name='credit_del'),
	url(r'^payment/(?P<client_id>[0-9]+)/$', views.payment, name='payment'),
	url(r'^payment/add/(?P<credit_id>[0-9]+)/$', views.payment_add, name='payment_add'),
	url(r'^payment/edit/(?P<id>[0-9]+)/$', views.payment_edit, name='payment_edit'),
	url(r'^payment/del/(?P<id>[0-9]+)/$', views.payment_del, name='payment_del'),
	url(r'^ledger/add/$', views.ledger_add, name='ledger_add'),
	url(r'^ledger/edit/(?P<id>[0-9]+)/$', views.ledger_edit, name='ledger_edit'),
	url(r'^ledger/del/(?P<id>[0-9]+)/$', views.ledger_del, name='ledger_del'),
]