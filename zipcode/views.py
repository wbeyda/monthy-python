from django.shortcuts import render
from django.http import HttpResponseRedirect
from zipcode.models import * 
from zipcode.forms import *
from django.core.mail import send_mail
from zipcode.calendars import * 
from django.views.generic.detail import DetailView

def results(request, postcode):
    con = Contractor.objects.filter(areacode=postcode).prefetch_related().order_by("lastname")
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

def request_event(request):
    if request.method == "POST":
        requested_event = ContractorScheduleForm(request.POST)
        if requested_event.is_valid():
            requested_event.save()
            return HttpResponseRedirect('schedule/')
        else:
            requested_event = ContractorScheduleForm(request.POST)
        return render(request, 'request_event.html', {'requested_event':requested_event})
    else:
        requested_event = ContractorScheduleForm(request.POST)
    return render(request, 'request_event.html', {'requested_event':requested_event})

def contractor_detail_view(request, f,id,l):
    con = Contractor.objects.filter(id=id).prefetch_related()
    htmlcalendar = contractor_calendar(con)
    return render(request, 'contractor_detail.html', {'con': con, 'htmlcalendar': htmlcalendar })

