from django.template.loader import get_template
from django import template
from zipcode import views
from zipcode.models import Testimonial

register = template.Library()

def show_contact_form():
	contactform = views.ContactForm
	return {'contactform': contactform}

register.inclusion_tag('contact.html')(show_contact_form)

def show_search_form():
	form = views.ZipForm
	return {'form': form}

register.inclusion_tag('search.html')(show_search_form)

def show_contractor_schedule_form():
	schedule = views.ContractorScheduleForm
	return {'schedule': schedule}

register.inclusion_tag('search.html')(show_contractor_schedule_form)

def show_testimonials():
	return {'testimonials': Testimonial.objects.all() }

register.inclusion_tag('testimonials.html')(show_testimonials)
