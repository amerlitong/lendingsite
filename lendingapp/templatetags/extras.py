from django import template

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