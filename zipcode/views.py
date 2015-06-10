from django.shortcuts import render
from django.http import HttpResponseRedirect
from zipcode.models import * 
from zipcode.forms import *
from django.core.mail import send_mail
from zipcode.calendars import * 
from django.views.generic.detail import DetailView

def results(request, postcode):
    con = Contractor.objects.filter(areacode=postcode).prefetch_related().order_by("lastname")
    cal = {}
    
    for s in con:   
        eventdict = {}  
        conevents = s.contractorschedule_set.all().order_by("firstname__lastname") 
        counter = conevents.count() #2
        n = 1
        for i in conevents:
            y,m = i.start_date.year,i.start_date.month
            event = "<ul><li>" + i.start_date.strftime("%I:%M")+" "+ i.title +" "+ i.end_date.strftime("%I:%M") +"</li></ul>"
            #loop through the days of the month
            for j in range(1,monthrange(y,m)[1]+1): #1-31                           
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
        setattr(s, 'contractorschedule', ContractorScheduleForm() )

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
            return HttpResponseRedirect('/thanks')
        else:
            requested_event = ContractorScheduleForm(request.POST)
        return render(request, 'results.html', {'requested_event':requested_event})
    else:
        requested_event = ContractorScheduleForm(request.POST)
    return render(request, 'results.html', {'requested_event':requested_event})

def contractor_calendar(queryset):
    for s in queryset:   
        eventdict = {}  
        conevents = s.contractorschedule_set.all() 
        counter = conevents.count() #2
        n = 1
        for i in conevents:
            y,m = i.start_date.year,i.start_date.month
            event = "<ul><li>" + i.start_date.strftime("%I:%M")+" "+ i.title +" "+ i.end_date.strftime("%I:%M") +"</li></ul>"
            #loop through the days of the month
            for j in range(1,monthrange(y,m)[1]+1): #1-31                           
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
    return htmlcalendar

def contractor_detail_view(request, id):
    con = Contractor.objects.prefetch_related().filter(pk=id)
    form = ContractorScheduleForm()
    htmlcalendar = contractor_calendar(con)
    print r"con\n",con,r"\n form\n", form, r"\n htmlcalendar \n", htmlcalendar 

    return render(request, 'contractor_detail.html', {'con': con, 'form': form, 'htmlcalendar': htmlcalendar })

