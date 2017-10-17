from django import template

register = template.Library()

@register.filter
def percent(value):
	return '{} %'.format(value*100)

@register.filter
def sub(value,arg):
	if arg:
		return value - arg
	else:
		return value

@register.filter
def inlist(value,lst):
	if value in lst:
		return True