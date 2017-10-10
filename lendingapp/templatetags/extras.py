from django import template
from datetime import datetime, date
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def percent(value):
	return '{} %'.format(value*100)

@register.filter
def sub(value,arg):
	return value - arg

@register.filter
def inlist(value,lst):
	if value in lst:
		return True

def date_to_str(value,format):
	return value.strftime(format)

@register.filter
def current_date(value):
	if value:
		return date_to_str(datetime.strptime(str(value),"%Y-%m-%d"),"%Y-%m-%d")
	return date_to_str(date.today(),"%Y-%m-%d")

@register.simple_tag
def input_control(type,name,value):
	d = dict(type=type,name=name,name1=name.upper(),value=value)
	s = '''<input class="form-control" type={type} step=0.001 id={name} placeholder={name1} name={name} value={value}>'''.format(**d)
	return mark_safe(s)