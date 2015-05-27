from django.template.loader import get_template
from django import template
from zipcode import views

register = template.Library()

def show_contact_form():
	contactform = views.ContactForm
	return {'contactform': contactform}

register.inclusion_tag('contact.html')(show_contact_form)

def show_search_form():
	form = views.ZipForm
	return {'form': form}

register.inclusion_tag('search.html')(show_search_form)