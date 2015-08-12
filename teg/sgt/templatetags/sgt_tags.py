from django import template

import string

register = template.Library()

@register.assignment_tag
def get_form_input(form, field, index):
	aux = field + '_' + str(index)
	return form[aux]

@register.filter(name='get_dict_val')
def get_dict_val(value, arg):
	aux = ''
	if value.has_key(arg):
		aux =  value[arg]

	return aux