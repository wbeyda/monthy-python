import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.text import Truncator

class Contractor(models.Model):
	areacode = models.PositiveIntegerField(max_length=5)
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	trade = models.CharField(max_length=20)
	secondaryTrades = models.CharField(max_length=200)
	bio = models.TextField()
	pic = models.ImageField(upload_to = 'photos/%Y/%m/%d')
	
	def __unicode__(self):
		return self.firstname + ' ' + self.lastname

class CareerResume(models.Model):
	name = models.CharField(max_length=20)
	address = models.CharField(max_length=20)
	email = models.EmailField()
	phone = models.IntegerField(max_length=10)
	resume = models.FileField(upload_to='files/%Y/%m/%d')

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
class ContractorSchedule(models.Model):
    firstname = models.ForeignKey(Contractor)
    start_date = models.DateTimeField(verbose_name=_("start date"))
    end_date = models.DateTimeField(_("end date"))
    all_day = models.BooleanField(_("all day"), default=False)
    title = models.CharField(_("title"), max_length=255, blank=True)
    description = models.TextField(_("description"),blank=True)
    location = models.ManyToManyField('Location', verbose_name=_('locations'), blank=True)
    background_color = models.CharField(
        _("background color"), max_length=10, choices=EVENT_COLORS, default='eeeeee'
    )
    def dispatch_number(self):
        import pdb; pdb.set_trace()
        pk = str(self.pk).zfill(5)
        self.pk = int(pk)
        return self.pk

    def __str__(self):
        return self.title
    
    def start_date_before_now(self):
        if self.start_date != None and self.start_date < timezone.now():
            raise ValidationError('Start Date cannot be before now')

    def end_date_before_start_date(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start date must be before the end date')

    def is_chunk(self):
        if self.start_date.day != self.end_date.day:
            raise ValidationError('Please enter these chunks of days as seperate Schedule Requests')
   
    def double_booked(self):
        qs = ContractorSchedule.objects.filter(
                                                firstname_id = self.firstname_id
                                              ).filter(
                                                      start_date__lte = self.start_date
                                                      ).filter(
                                                              end_date__gte = self.start_date
                                                              )
        if qs.exists():
            for i in qs:
                if not self.start_date - i.end_date == datetime.timedelta(0):     
                    raise ValidationError(_('Double Booking! job number: %(value)s'),
                                   code="double-booked",
                                   params = {'value': i.id},
                                  )

    def two_hour_blocks(self):
        if self.start_date.day == self.end_date.day:
            block = self.end_date - self.start_date
            
            if block < datetime.timedelta(0, 7200):
                raise ValidationError(_('Block is under 2 hours'), code="short-block")        
        
    def clean(self):
        #self.start_date_before_now()
        self.double_booked()
        self.two_hour_blocks()
        self.end_date_before_start_date()
        #self.is_chunk()
        #self.dispatch_number()

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
    name = models.CharField(_('Name'), max_length=255)
    address_line_1 = models.CharField(
        _('Address Line 1'), max_length=255, blank=True)
    address_line_2 = models.CharField(
        _('Address Line 2'), max_length=255, blank=True)
    address_line_3 = models.CharField(
        _('Address Line 3'), max_length=255, blank=True)
    state = models.CharField(
        _('State / Province / Region'), max_length=63, blank=True)
    city = models.CharField(
        _('City / Town'), max_length=63, blank=True)
    zipcode = models.CharField(
        _('ZIP / Postal Code'), max_length=31, blank=True)
    country = models.CharField(_('Country'), max_length=127, blank=True)

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
            return self.testimonial.customer_name 

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
            self.author = self.testimonial.customer_name
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
    customer_name        = models.CharField(_('customer name'), max_length=255)
    customer_city        = models.CharField(_('customer city'), max_length=255)
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
        return self.customer_name 

    def image_tag(self):
        return u'<img class="admin_img_preview" style="max-height:20em;" src=' + self.job_pic.url +'/>'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True   

TEXT_COLORS = [
        ('000000', _('black')),
        ('ffffff', _('white')),
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




