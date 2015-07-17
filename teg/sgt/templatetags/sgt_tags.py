from django import template

import string

register = template.Library()

@register.assignment_tag
def get_form_input(form, field, index):
	aux = field + '_' + str(index)
	return form[aux]
