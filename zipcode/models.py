import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.utils.text import Truncator
from django.contrib.auth.models import User

from image_cropping import ImageRatioField

from localflavor.us.models import PhoneNumberField
from localflavor.us.models import USZipCodeField 
from localflavor.us.models import USStateField 



class Contractor(models.Model):
    user = models.ForeignKey(User, unique=True)
    areacode = models.PositiveIntegerField(max_length=5)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    trade = models.CharField(max_length=20)
    secondaryTrades = models.CharField(max_length=200)
    bio = models.TextField()
    pic = models.ImageField(upload_to = 'photos/%Y/%m/%d')
    cropping = ImageRatioField('pic', '400x400')
	
    def __unicode__(self):
        return self.firstname + ' ' + self.lastname

    def image_tag(self):
        return u'<img class="admin_img_preview" style="max-height:20em;" src=' + self.pic.url +'/>'

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True 

class Customer(models.Model):
    first_name         = models.CharField(max_length=20)
    last_name          = models.CharField(max_length=20)
    email              = models.CharField(max_length=254)
    phone_number       = PhoneNumberField()
    address_line_1     = models.CharField(max_length=200)
    address_line_2     = models.CharField(max_length=200, blank=True)
    city               = models.CharField(max_length=200)
    state              = USStateField() 
    zipcode            = USZipCodeField() 
    subscribed         = models.BooleanField(default=True)
    special_notes      = models.TextField(default='', blank=True)

    def __unicode__(self):
        print self.phone_number
        return unicode(self.phone_number)

class CareerResume(models.Model):
    name    = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    email   = models.EmailField(max_length=254)
    phone   = models.IntegerField(max_length=10)
    resume  = models.FileField(upload_to='files/%Y/%m/%d')


class ContractorSchedule(models.Model):
    firstname    = models.ForeignKey(Contractor)
    customer     = models.OneToOneField(Customer)
    start_date   = models.DateTimeField(verbose_name=_("start date"))
    end_date     = models.DateTimeField(_("end date"))
    repair       = models.BooleanField(_('repair'), default=False )
    estimate     = models.BooleanField(_('estimate'), default=False )
    installation = models.BooleanField(_('installation'), default=False )
    maintenance  = models.BooleanField(_('Preventitive Maintenance'), default=False )
    all_day      = models.BooleanField(_("all day"), default=False)
    emergency    = models.BooleanField(_("Emergency"), default=False)
    value_care   = models.BooleanField(_("Value Care"), default=False)
    title        = models.CharField(_("title"), max_length=255, blank=True)
    description  = models.TextField(_("description"),blank=True)
    location     = models.ManyToManyField('Location', verbose_name=_('locations'), blank=True)
    completed    = models.BooleanField(_('completed'), default=False)
    pending      = models.BooleanField(_('pending'), default=True)
    approved     = models.BooleanField(_('approved'), default=False)


    def dispatch_number(self):
        pk = str(self.pk).zfill(5)
        self.pk = int(pk)
        return self.pk

    def __str__(self):
        return self.title
    
    def start_date_before_now(self):
        if self.start_date != None and self.start_date < timezone.now():
            raise ValidationError(_('Start Date cannot be before now'),
                                 code="#id_start_date_0", 
                                  )

    def clean_seconds(self):
        s = self.start_date 
        if s is None:
            return self
        self.start_date = s.replace( second=0, microsecond=0)
        e = self.end_date
        self.end_date = e.replace( second=0, microsecond=0)
        return self 

    def end_date_before_start_date(self):
        if self.start_date is not None and self.start_date >= self.end_date:
            raise ValidationError(_('Start date must be before the end date'),
                                code = "#id_end_date_0"
                                )

    def is_chunk(self):
        if self.start_date.day is not None and self.start_date.day != self.end_date.day:
            raise ValidationError('Please enter these chunks of days as seperate Schedule Requests')
   
    def double_booked(self):
        #import pdb; pdb.set_trace()
        qs = ContractorSchedule.objects.filter(firstname_id = self.firstname_id,
                                               start_date__lte = self.start_date,
                                               end_date__gte = self.start_date,
                                               end_date__lt = self.end_date,)
        #----[1](2)[3][4](5)----
        if qs.exists():
            for i in qs:
                if not self.start_date - i.end_date == datetime.timedelta(0):     
                    raise ValidationError(_('Double Booking! job number: %(value)s'),
                                          code="#id_start_date_0",
                                          params = {'value': i.id},
                                         )
        qs = ContractorSchedule.objects.filter(firstname_id = self.firstname_id,
                                               start_date__gte = self.start_date,
                                               start_date__lte = self.end_date,
                                               end_date__gte = self.start_date,)
        
        #---(1)[2][3](4)[5]----
        if qs.exists():
            for i in qs:
                if not self.start_date - i.end_date == datetime.timedelta(0):     
                    raise ValidationError(_('Double Booking! job number: %(value)s'),
                                          code="#id_start_date_0",
                                           params = {'value': i.id},
                                          )
        qs = ContractorSchedule.objects.filter(firstname_id = self.firstname_id,
                                               start_date__gte = self.start_date,
                                               end_date__lte = self.end_date,)
        
        #----(1)[2][3][4][5](6)----
        if qs.exists():
            for i in qs:
                if not self.start_date - i.end_date == datetime.timedelta(0):     
                    raise ValidationError(_('Double Booking! job number: %(value)s'),
                                          code="#id_start_date_0",
                                           params = {'value': i.id},
                                          )
        qs = ContractorSchedule.objects.filter(firstname_id = self.firstname_id,
                                               start_date__lte = self.start_date,
                                               end_date__gte = self.end_date,)
        
        #----[2](3)(4)[5]----
        if qs.exists():
            for i in qs:
                if not self.start_date - i.end_date == datetime.timedelta(0):     
                    raise ValidationError(_('Double Booking! job number: %(value)s'),
                                          code="#id_start_date_0",
                                           params = {'value': i.id},
                                          )


    def two_hour_blocks(self):
        if self.start_date.day == self.end_date.day and self.start_date < self.end_date:
            block = self.end_date - self.start_date
            
            if block < datetime.timedelta(0, 7200):
                raise ValidationError(_('Block is under 2 hours'),
                                       code="#id_start_date_1")        
    
    def multiple_days(self):
        if self.start_date.day < self.end_date.day and self.all_day == False:
            raise ValidationError(_('Please check All day if this is multiple days'), code="#id_all_day")    

    def all_day_double(self):
        if self.all_day == True:
            st = self.start_date
            newStartDate = datetime.datetime(st.year, st.month, st.day,0,0)
            newEndDate =   datetime.datetime(st.year, st.month, st.day, 23,59) 
            qs = ContractorSchedule.objects.filter(firstname_id = self.firstname_id
                                                  ).filter(all_day = True
                                                  ).filter(start_date__gt = newStartDate
                                                  ).filter(start_date__lt = newEndDate)
                                                  
            if qs.exists():
                raise ValidationError(_('This day is already booked all day.'), code="#id_all_day")

    def day_is_full(self):
        st = self.start_date
        newStartDate = datetime.datetime(st.year, st.month, st.day,0,0)
        newEndDate =   datetime.datetime(st.year, st.month, st.day, 23,59) 
        qs = ContractorSchedule.objects.filter(firstname_id = self.firstname_id
                                              ).filter(all_day = True
                                              ).filter(start_date__gt = newStartDate
                                              ).filter(start_date__lt = newEndDate)
                                                  
        if qs.exists():
            raise ValidationError(_('This day is already full.'), code="#id_start_date_0")

    def before_prefered_start_time(self):
        #import pdb; pdb.set_trace()
        a = Availability.objects.get(id=self.firstname_id)
        pst = a.prefered_starting_hours #datetime.time(9,0) 
        stt = datetime.time(self.start_date.hour, self.start_date.minute)
        if datetime.datetime.combine(datetime.datetime.today(), pst) > datetime.datetime.combine(datetime.datetime.today(), stt) == False: 
            raise ValidationError(_('This is before the Contractors prefered starting hour. An email has been sent to ask for permission'),
                                     code='#id_start_date_1')

    def after_prefered_end_time(self):
        a = Availability.objects.get(id=self.firstname_id)
        pet = a.prefered_ending_hours #datetime.time(17,0) 
        seh = datetime.time(self.end_date.hour, self.end_date.minute)
        if datetime.datetime.combine(datetime.datetime.today(), pet) < datetime.datetime.combine(datetime.datetime.today(), seh) == False: 
            raise ValidationError(_('This is after the Contractors prefered ending hour. An email has been sent to ask for permission'),
                                     code='#id_end_date_1')
    
    def clean(self):
        self.start_date_before_now()
        self.clean_seconds()
        self.double_booked()
        self.two_hour_blocks()
        self.end_date_before_start_date()
        self.is_chunk()
        self.multiple_days()        
        self.all_day_double()
        self.day_is_full()

    def save(self, *args, **kwargs):
        super(ContractorSchedule, self).save(*args, **kwargs)
        try:
            self.before_prefered_start_time()
        except ValidationError as e:
            return e
        try:
            self.after_prefered_end_time()
        except ValidationError as e:
            return e
            

HOURS = ['Midnight','12:15AM','12:30AM,12:45AM']

class Availability(models.Model):
    contractor              = models.ForeignKey(Contractor)
    evenings                = models.BooleanField(default=False)
    weekends                = models.BooleanField(default=False)
    prefered_starting_hours = models.TimeField(verbose_name = _("Prefered starting time"))
    prefered_ending_hours   = models.TimeField(verbose_name = _("Prefered ending time"))
    anytime                 = models.BooleanField(default=False)
    prefered_zipcodes       = models.CommaSeparatedIntegerField(max_length=255)

    def __unicode__(self):
        contractor_name = self.contractor.firstname +' ' + self.contractor.lastname
        return contractor_name

		
class Location(models.Model):
    name           = models.CharField(_('Name'), max_length=255)
    address_line_1 = models.CharField(_('Address Line 1'), max_length=255, blank=True)
    address_line_2 = models.CharField(_('Address Line 2'), max_length=255, blank=True)
    address_line_3 = models.CharField(_('Address Line 3'), max_length=255, blank=True)
    state          = models.CharField(_('State / Province / Region'), max_length=63, blank=True)
    city           = models.CharField(_('City / Town'), max_length=63, blank=True)
    zipcode        = models.CharField(_('ZIP / Postal Code'), max_length=31, blank=True)
    country        = models.CharField(_('Country'), max_length=127, blank=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    picture     = models.FileField(upload_to='gallery/%Y/%m/%d', blank=True, help_text="select your own or select a Testimonial with a pic")
    caption     = models.CharField(_('caption'),max_length=3000, blank=True, help_text="write your own or select a Customers Testimonial")
    author      = models.CharField(_('author'), max_length=255, blank=True,  help_text="Who is the pic Author? or select a Testimonial")
    sourceURL   = models.URLField(_('source URL'), blank=True,               help_text="paste the URL or let me get it from a Testimonial")
    picdate     = models.DateTimeField(_("pic date"), blank=True,            help_text="select the date for this job or just select a Testimonial" )
    contractor  = models.ForeignKey(Contractor)
    job         = models.ForeignKey(ContractorSchedule, default=00000)
    hashtags    = models.CharField(_('hashtags'), max_length=255, blank=True, default=None)
    socialtags  = models.CharField(_('socialtags'), max_length=255, blank=True, default=None)
    testimonial = models.ForeignKey('Testimonial', blank=True, default=None)

    def __str__(self):
        if self.author is not None:
            return self.author
        else:
            return self.testimonial.customer 

    def picture_is_job_pic(self):
        if self.testimonial != None and not self.picture:
            self.picture = self.testimonial.job_pic
        return self.picture
 
    def caption_is_customer_testimonial(self):
        if self.testimonial != None and self.caption == u'':
            self.caption = self.testimonial.customer_testimonial
        return self.caption

    def author_is_customer_name(self):
        if self.testimonial != None and self.author == u'':
            self.author = self.testimonial.customer
        return self.author

    def sourceurl_is_job_pic_url(self):
        if self.testimonial != None and self.sourceURL == u'':
            self.sourceURL = self.testimonial.job_pic_url
        return self.sourceURL  

    def picdate_is_customer_date(self):
        if self.testimonial != None and self.picdate == None:
            self.picdate = self.testimonial.customer_date
        return self.picdate

    def hashtags_from_testimonials(self):
        if self.testimonial != None and self.hashtags == u'':
            self.hashtags = self.testimonial.hashtags
        return self.hashtags

    def socialtags_from_testimonials(self):
        if self.testimonial is not None and self.socialtags == u'':
            self.socialtags = self.testimonial.socialtags
        return self.socialtags

    def contractor_from_testimonials(self):
        if self.testimonial is not None:
            try:
               self.contractor 
            except Contractor.DoesNotExist:
                self.contractor = self.testimonial.contractor
                return self.contractor
 
    def clean(self):
        self.picture_is_job_pic() 
        self.caption_is_customer_testimonial()
        self.author_is_customer_name() 
        self.sourceurl_is_job_pic_url() 
        self.picdate_is_customer_date()
        self.hashtags_from_testimonials()
        self.socialtags_from_testimonials()
        self.contractor_from_testimonials() 

  
class Testimonial(models.Model):
    customer             = models.ForeignKey(Customer)
    customer_testimonial = models.TextField(_('customer testimonial'))
    customer_date        = models.DateTimeField(_("customer date"), auto_now_add=True)
    contractor           = models.ForeignKey(Contractor)
    job                  = models.ForeignKey(ContractorSchedule, unique=True)
    job_pic              = models.FileField(upload_to='testimonial/%Y/%m/d/%H%M')
    job_pic_url          = models.CharField(_('job pic url'), max_length=255, blank=True)
    hashtags             = models.CharField(_('hashtags'), max_length=255, blank=True)
    socialtags           = models.CharField(_('socialtags'), max_length=255, blank=True)
    approved_status      = models.BooleanField(default=False)
    best_of              = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.customer) 

    def image_tag(self):
        return u'<img class="admin_img_preview" style="max-height:20em;" src=' + self.job_pic.url +'/>'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True   

    def customer_job_mismatch(self):
        import pdb; pdb.set_trace()
        if self.customer.id != self.job.customer.id: 
            raise ValidationError(_("Customer Job Mismatch"), code="wrong job")
    def clean(self):
        self.customer_job_mismatch()

TEXT_COLORS = [
        ('000000', _('black')),
        ('ffffff', _('white')),
    ]

EVENT_COLORS  = [
        ('eeeeee', _('gray')),
        ('777777', _('dark-gray')),
        ('ef3b70', _('red')),
        ('2ebad1', _('blue')),
        ('85d4f5',_('light-blue')),
        ('57b449', _('green')),
        ('000000', _('black')),
        ('ffffff', _('white')),
        ('fcda09', _('yellow')),
    ]

class MonthlySpecial(models.Model):
    special_pic          = models.FileField(upload_to='specials/%Y/%m/%d', blank=True, help_text="please make sure all images are the same width")
    special_text         = models.CharField( _('Special Text'), max_length=255)
    special_details      = models.TextField( _('Special Details'), default="",)
    special_color        = models.CharField(choices=EVENT_COLORS, max_length=7)
    special_text_color   = models.CharField(choices=TEXT_COLORS, max_length=7, default="000000")
    special_active       = models.BooleanField(_('Is Special Active?'), default=True)
    special_pic_alt_text = models.CharField(_('Special Pic Alt Text'), default='monthly special picture', max_length=255)
    special_url          = models.CharField(_('Special URL'), default= "", max_length=255, blank=True)

    def __unicode__(self):
        return self.special_text
    
    def slugify_text(self):
        if self.special_url == u'':
            shorter_text = Truncator(self.special_text).words(10)
            self.special_url = slugify(shorter_text)
        return self.special_url

    def clean(self):
        self.slugify_text()

    def image_tag(self):
        preview_image =u'<img class="admin_img_preview" style="max-height:20em;" src=' + self.special_pic.url + '/>'
        return preview_image

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True 
