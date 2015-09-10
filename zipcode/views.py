from django.shortcuts import render
import json, itertools, datetime
from django.http import HttpResponseRedirect
from django.http import HttpRequest, HttpResponse 
from zipcode.models import * 
from zipcode.forms import *
from django.core.mail import send_mail
from zipcode.calendars import * 
from django.views.generic.detail import DetailView
from django.core import serializers


def day_or_night():
    if datetime.datetime.now().time().hour < 17:
        time_image = 'day'
    else:
        time_image = 'night'
    return time_image


def home(request):
    time_image = day_or_night()
    testimonials = Testimonial.objects.filter(best_of=True)
    monthly_specials = MonthlySpecial.objects.filter(special_active=True)
    return render(request, 'home.html', {'time_image': time_image, 'testimonials': testimonials, 'monthly_specials': monthly_specials})

def monthly_special_detail(request, id, special):
    time_image = day_or_night()
    monthly_special = MonthlySpecial.objects.get(id = id)
    return render(request, 'monthly_special_detail.html', {'monthly_special': monthly_special, 'time_image': time_image})

def results(request, postcode):
    con = Contractor.objects.filter(areacode=postcode).prefetch_related().order_by("lastname")
    time_image = day_or_night()
    return render(request, 'results.html', {'con': con, 'time_image': time_image})


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
            contactform = ContactForm(auto_id="contact_%s")
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
    time_image = day_or_night 
    return render(request, 'careers.html', {'careerform':careerform, 'time_image': time_image})


def show_gallery(request):
    gallery = Gallery.objects.all().prefetch_related()
    time_image = day_or_night() 
    return render(request, 'gallery.html', {'gallery':gallery,'time_image': time_image})


def request_event(request):
    time_image = day_or_night()
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
    return render(request, 'request_event.html', {'requested_event':requested_event,'time_image': time_image})

    
def calendar_manager_cells( year, month, uid):
    #import pdb; pdb.set_trace()
    fdom = datetime.datetime(year, int(month), 1,0)

    if month == 12:
        ldom = datetime.datetime(year+1,1,1,0)
    else:
        ldom = datetime.datetime(year,int(month)+1,1,0)
    
    cal_query = ContractorSchedule.objects.filter(firstname_id =int(uid), start_date__gte = fdom, end_date__lt = ldom)
    av = Availability.objects.get(contractor_id=int(uid))
    sh = av.prefered_starting_hours
    eh = av.prefered_ending_hours  
    ah = datetime.datetime.combine(date.today(), eh) - datetime.datetime.combine(date.today(), sh)
    avail_hours = ah.total_seconds() / 3600 #8.0 or 8.5
    alldays = cal_query.filter(all_day = True)
    full_days = []
    
    for i in alldays: #if the first day of a chunk starts at the begining of Availability add it to full days in full_days
        chunk_of_days = list(range(i.start_date.day, i.end_date.day))
        if chunk_of_days > 0:
            psh = datetime.datetime.combine(i.start_date, sh)
        if psh == i.start_date:
            full_days.append(i.start_date.day)
   
    for i in chunk_of_days[1:]: #add the rest of the days from a chunk to full_days 
        full_days.append(i)


    for i in cal_query:
        full_days.append(i.start_date.day)

    a = [elem for elem in full_days if elem >= avail_hours /2]
    full_days_in_this_month = []
    [full_days_in_this_month.append(item) for item in a if item not in full_days_in_this_month]
    return full_days_in_this_month 


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


def calendar_manager_blocks(request, currentdate, uid, currentyear, currentmonth):

    #import pdb; pdb.set_trace()
    if request.is_ajax():
        today = datetime.datetime(int(currentyear),int( currentmonth), int(currentdate), 0)
        import calendar
        last_day_of_month  = calendar.monthrange(int(currentyear), int(currentmonth))[1]
        if int(currentdate) == last_day_of_month and int(currentmonth) == 12: 
            tomorrow = datetime.datetime(int(currentyear)+1, 1,1,0)
        elif int(currentdate) == last_day_of_month and int(currentmonth) <= 11:
            tomorrow = datetime.datetime(int(currentyear), int(currentmonth)+1, 1, 0)
        else:  
            tomorrow = datetime.datetime(int(currentyear), int(currentmonth), int(currentdate)+1, 0)
        uid = int(uid)
        all_the_days = []

        calendardays = ContractorSchedule.objects.filter(firstname_id=uid, 
                                                         start_date__gte = today,
                                                         end_date__lt = tomorrow
                                                        ).order_by('start_date')

        first_day_of_chunks_of_days = ContractorSchedule.objects.filter(firstname_id = uid,
                                                           start_date__gte = today,
                                                           all_day = True,
                                                           start_date__lte = tomorrow
                                                           ).order_by('start_date')

        middle_of_a_chunk_of_days = ContractorSchedule.objects.filter(firstname_id = uid, 
                                                                      start_date__lte = today, 
                                                                      end_date__gte = tomorrow,
                                                                      all_day = True,
                                                                     ).order_by('start_date')

        end_of_a_chunk_of_days = ContractorSchedule.objects.filter(firstname_id = uid,
                                                                   end_date__gte = today,
                                                                   end_date__lte = tomorrow,
                                                                   all_day = True,
                                                                  ).order_by('start_date') 
        
       
        if first_day_of_chunks_of_days.exists():
           all_the_days.append(first_day_of_chunks_of_days)
        else :
            first_day = ""
            all_the_days.append(first_day) 

        if middle_of_a_chunk_of_days.exists():
            all_the_days.append(middle_of_a_chunk_of_days)
        else:
            middle = ""
            all_the_days.append(middle)
        
        if end_of_a_chunk_of_days.exists():
            all_the_days.append( end_of_a_chunk_of_days) 
        else:
            end = ""
            all_the_days.append( end)
        
        if calendardays.exists():
            all_the_days.append(calendardays)
        else:
            caldays = ""
            all_the_days.append( caldays )
        
        filtered_days = [elem for elem in all_the_days if elem != ""]
        all_days = list(itertools.chain(filtered_days[0]))
        data = serializers.serialize('json', all_days, use_natural_keys=True ) 
        
        #data = json.dumps({ 'first_day': first_day, 'middle': middle, 'end': end , 'caldays': caldays })

        return HttpResponse(data, content_type="application/json")
   

def contractor_detail_view(request, f,id,l):
    con = Contractor.objects.filter(id=id).prefetch_related()
    avail = Availability.objects.filter(contractor_id=id).prefetch_related()
    avail = serializers.serialize("json", avail)
    testimonials = Testimonial.objects.filter(contractor_id=id).prefetch_related().exclude(approved_status=False)
    htmlcalendar = contractor_calendar(con)
    from django.forms.models import inlineformset_factory
    conschedule = ContractorSchedule.objects.filter(firstname_id=id)
    testimonial_form = testimonialform_factory(conschedule)
    time_image = day_or_night()
    monthly_specials = MonthlySpecial.objects.filter(special_active=True)
    cal_man_cells = calendar_manager_cells( datetime.datetime.today().year, datetime.datetime.today().month, id)
    
    return render(request, 'contractor_detail.html', {'con': con, 
                                                      'htmlcalendar': htmlcalendar, 
                                                      'testimonials': testimonials, 
                                                      'testimonial_form': testimonial_form,
                                                      'availability': avail,
                                                      'time_image': time_image,
                                                      'monthly_specials': monthly_specials,
                                                      'cal_man_cells': cal_man_cells
                                                      })
