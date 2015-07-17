from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpRequest, HttpResponse 
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

def post_testimonial(request, id):
    if request.method == 'POST':
        testimonial_form = TestimonialForm(request.POST,request.FILES)
        if testimonial_form.is_valid():
            import pdb; pdb.set_trace()
            newform = testimonial_form.save(commit=False)
            newform.contractor_id = id
            newform.approved_status = False
            newform.save()
            print("this posted")
            return HttpResponseRedirect('/thanks/')
        else:
            testimonial_form = TestimonialForm()
            return HttpResponse('error')

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
    gallery = Gallery.objects.all().prefetch_related()
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
    testimonials = Testimonial.objects.filter(contractor_id=id).prefetch_related().exclude(approved_status=False)
    htmlcalendar = contractor_calendar(con)
    from django.forms.models import inlineformset_factory
    '''testform = inlineformset_factory(ContractorSchedule,
                                    Testimonial,
                                    form=TestimonialForm,
                                    fk_name='job',fields=(
                                                            'customer_name',
                                                            'customer_city',
                                                            'customer_testimonial',
                                                            'job',
                                                            'job_pic',
                                                            'job_pic_url',
                                                            'hashtags',
                                                            'socialtags'))
    '''
    conschedule = ContractorSchedule.objects.filter(firstname_id=id)
    #testimonial_form = testform(instance=conschedule)
    testimonial_form = testimonialform_factory(conschedule)
    return render(request, 'contractor_detail.html', {'con': con, 'htmlcalendar': htmlcalendar, 'testimonials': testimonials, 'testimonial_form': testimonial_form})

def next_month_request(request, id, currentyear, currentmonth):
    if request.is_ajax():
        if int(request.GET.get('currentmonth')) == 12:
            nextyear = int(request.GET.get('currentyear')) + 1
            qs = ContractorSchedule.objects.filter(firstname_id=int(id)).exclude(
                                                                            start_date__lt=datetime.datetime(
                                                                                int(currentyear),
                                                                                int(currentmonth),
                                                                                1)
                                                                        ).exclude(
                                                                        start_date__gt=datetime.datetime(nextyear,1,31,23,59,59))
            queryset = []
            for i in qs: 
                h,m =  i.start_date.hour, i.start_date.minute
                if i.start_date.month != i.end_date.month:
                    i.start_date = last_day_of_month(i.start_date) + datetime.timedelta(seconds=1)+ datetime.timedelta(hours=h) + datetime.timedelta(minutes=m)
                    queryset.append(i)
                else:
                    queryset.append(i)
            if queryset:
                htmlcalendar = next_last_month_contractor_calendar(queryset)
                return HttpResponse(htmlcalendar)
            else:
                htmlcalendar = LocaleHTMLCalendar().formatmonth(nextyear,1)
                return HttpResponse(htmlcalendar)
        elif int(request.GET.get('currentmonth')) != 12 :
            cid = int(request.GET.get("id"))     
            nextmonth = int(request.GET.get('currentmonth')) +1
            cy = int(request.GET.get('currentyear'))
            d = datetime.datetime(cy,nextmonth,1) 
            qs = ContractorSchedule.objects.filter(firstname_id=cid).exclude(
                          start_date__lt=first_day_of_month(datetime.datetime(cy,int(currentmonth),1))).exclude(
                          start_date__gt=last_day_of_month(d))
            queryset = []
            for i in qs:
                #import pdb; pdb.set_trace()
                h,m =  i.start_date.hour, i.start_date.minute
                if i.start_date.month < i.end_date.month and i.end_date.month == nextmonth:
                    i.start_date = last_day_of_month(i.start_date) + datetime.timedelta(seconds=1)+ datetime.timedelta(hours=h) + datetime.timedelta(minutes=m)
                    queryset.append(i)
                elif i.start_date.month == nextmonth: 
                    queryset.append(i)
            if not queryset:
                htmlcalendar = LocaleHTMLCalendar().formatmonth(cy,nextmonth) 
            else:
                htmlcalendar = next_last_month_contractor_calendar(queryset)
        return HttpResponse(htmlcalendar) 

def last_month_request(request, id, currentyear, currentmonth):
    if request.is_ajax():
        if int(request.GET.get("currentmonth")) == 1:
            lastyear = int(currentyear) -1
            qs = ContractorSchedule.objects.filter(firstname_id=int(request.GET.get("id"))).exclude(
                        start_date__gt=datetime.datetime(lastyear,12,31,23,59,59)).exclude(
                        end_date__lt=datetime.datetime(lastyear,11,1)  
                      )
            queryset = []
            for i in qs:
                h,m = i.start_date.hour, i.start_date.minute
                if i.end_date.month == 12 and i.start_date.month <= 12:
                    i.start_date = datetime.datetime(lastyear,12,1) + datetime.timedelta(hours=h) + datetime.timedelta(minutes=m)
                    queryset.append(i)
                else:
                    queryset.append(i)
            if not queryset:
                htmlcalendar = LocaleHTMLCalendar().formatmonth(lastyear, 12)
                return HttpResponse(htmlcalendar)
            else:
                htmlcalendar = next_last_month_contractor_calendar(queryset)
                return HttpResponse(htmlcalendar)
        elif int(request.GET.get("currentmonth")) != 1:
            lastmonth = int(request.GET.get("currentmonth")) -1
            cy = int(currentyear)
            d = datetime.datetime(cy,lastmonth,1)
            qs = ContractorSchedule.objects.filter(firstname_id=int(id)).exclude(
                           start_date__gt = last_day_of_month(d)).exclude(
                           end_date__lt = d)
            queryset = []
            
            for i in qs:
                h,m = i.start_date.hour, i.start_date.minute
                if i.end_date.month == lastmonth and i.start_date.month < lastmonth: 
                    i.start_date = last_day_of_month(i.start_date) + datetime.timedelta(seconds=1)+ datetime.timedelta(hours=h) + datetime.timedelta(minutes=m)
                    queryset.append(i)
                elif i.start_date.month == lastmonth:
                    queryset.append(i)
            if not queryset:
                htmlcalendar = LocaleHTMLCalendar().formatmonth(cy,lastmonth) 
                return HttpResponse(htmlcalendar)
            else:
                htmlcalendar = next_last_month_contractor_calendar(queryset)
                return HttpResponse(htmlcalendar)
