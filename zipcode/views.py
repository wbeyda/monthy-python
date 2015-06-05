from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
#from zipcode.models import Contractor, CareerResume, ContractorSchedule, Location, Gallery, Testimonials
from zipcode.models import * 
from django import forms
from zipcode.forms import *
from django.core.mail import send_mail
from calendar import LocaleHTMLCalendar, month_name, monthrange
from datetime import date


class GenericCalendar(LocaleHTMLCalendar):
	def __init__(self, year, month):
		super(GenericCalendar, self).__init__()
		self.yr = year
		self.mo = month

	def formatday(self, day, weekday, event):
		if day == 0:
			return '<td class="noday">&nbsp;</td>' # day outside month
		elif day != 0 and event[0][day] != None:
			return '<td class="%s">%d %s</td>' % (self.cssclasses[weekday], day, event[0][day])
		elif day !=0 and event[0][day] == None:
			return '<td class="%s">%d %s</td>' % (self.cssclasses[weekday], day, "")

	def formatweek(self, theweek, *event):                                                                      
		if len(event) == 0:                                                                                         
			s = ''.join(self.formatday(d, wd, event) for (d, wd) in theweek)                                               
		else:                                                                                                       
			s = ''.join(self.formatday(d, wd, event) for (d, wd) in theweek)                                       
		return '<tr>%s</tr>' % s

	def formatmonth(self, theyear, themonth, event, withyear=True):
		v = []
		a = v.append
		a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
		a('\n')
		a(self.formatmonthname(theyear, themonth, withyear=withyear))
		a('\n')
		a(self.formatweekheader())
		a('\n')
		for week in self.monthdays2calendar(theyear, themonth):
			a(self.formatweek(week, event))
			a('\n')
		a('</table>')
		a('\n')
		return ''.join(v)


def results(request, postcode):
	#con has every both Contractors (Jeffrey and Walter) each have 2 ContractorSchedule events
	con = Contractor.objects.filter(areacode=postcode).prefetch_related().order_by("lastname")
	cal = {}
	
	for s in con:	
		eventdict = {}	
		conevents = s.contractorschedule_set.all().order_by("firstname__lastname") #<ContractorSchedule: ContractorSchedule object>, <ContractorSchedule: ContractorSchedule object>
		counter = conevents.count() #2
		n = 1
		for i in conevents:
			y,m = i.start_date.year,i.start_date.month
			event = "<ul><li>" + i.start_date.strftime("%I:%M")+" "+ i.title +" "+ i.end_date.strftime("%I:%M") +"</li></ul>"
			#loop through the days of the month
			for j in range(1,monthrange(y,m)[1]+1):	#1-31				
				if i.start_date.day == j and j not in eventdict:
					eventdict[j] = event
				elif j not in eventdict:
					eventdict[j] = None
				#add to a day with an event
				if i.start_date.day == j and eventdict[j] != "" and eventdict[j] is not None and eventdict[j] != event:
					eventdict[j] += event
				#change day from none to event 
				if i.start_date.day == j and eventdict[j] is None:
					eventdict[j] = event
				if j == monthrange(y,m)[1] and n == counter:
					htmlcalendar = GenericCalendar(y,m).formatmonth(y,m, eventdict)
				elif j == monthrange(y,m)[1] and n != counter:
					n+=1
		setattr(s, 'htmlcalendar', htmlcalendar)
		setattr(s, 'contractorschedule', ContractorScheduleForm( initial={"firstname": s.firstname} ) )

	return render(request, 'results.html', {'con': con})


def get_zip(request):
	if request.method == 'POST':
		form = ZipForm(request.POST)
		if form.is_valid():				
			return HttpResponseRedirect('/search/' + request.POST['zipsearch'])
	else:
		form = ZipForm()
	return render(request, 'search.html', {'form': form})


def get_contact(request):
	if request.method == 'POST':
		contactform = ContactForm(request.POST)
		if contactform.is_valid():
			message = "{name} / {address} / {email} said: ".format(
				name=contactform.cleaned_data.get('name'),
				address=contactform.cleaned_data.get('address'),
				email=contactform.cleaned_data.get('email'))
			message += "\n\n{0}".format(contactform.cleaned_data.get('problem'))
			send_mail(
				subject=contactform.cleaned_data.get('name').strip(),
				message=message,
				from_email='wbeyda@gmail.com',
				recipient_list=['wbeyda@gmail.com'],
			)				
			return HttpResponseRedirect('/thanks/')
	else:
		contactform = ContactForm()
	return render(request, 'contact.html', {'contactform': contactform})

def validate_file_extension(value):
	import os
	ext = os.path.splitext(value.name)[1]
	valid_extensions = ['.pdf','.doc','.docx']
	if not ext in valid_extensions:
		raise ValidationError(u'File not supported!')


def handle_uploaded_file(f):
	with open(f, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def get_resume(request):
	if request.method == 'POST':
		careerform = CareerForm(request.POST, request.FILES)
		if careerform.is_valid():
			careerform.save()
			return HttpResponseRedirect('/thanks')
		else:
			careerform = CareerForm()
		return render(request, 'careers.html', {'careerform':careerform})
	else:
		careerform = CareerForm()
	return render(request, 'careers.html', {'careerform':careerform})

def show_gallery(request):
	gallery = Gallery.objects.all()
	return render(request, 'gallery.html', {'gallery':gallery})

