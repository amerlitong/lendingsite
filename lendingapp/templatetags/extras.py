from django import template

register = template.Library()

@register.filter
def percent(value):
	return '{} %'.format(value*100)