import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError

class Contractor(models.Model):
	areacode = models.PositiveIntegerField(max_length=5)
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	trade = models.CharField(max_length=20)
	secondaryTrades = models.CharField(max_length=200)
	bio = models.TextField()
	pic = models.ImageField(upload_to = 'photos/%Y/%m/%d')
	
	def __str__(self):
		return self.firstname

class CareerResume(models.Model):
	name = models.CharField(max_length=20)
	address = models.CharField(max_length=20)
	email = models.EmailField()
	phone = models.IntegerField(max_length=10)
	resume = models.FileField(upload_to='files/%Y/%m/%d')

EVENT_COLORS  = [
        ('eeeeee', _('gray')),
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
    def clean(self):
	    #self.start_date_before_now()
	    self.end_date_before_start_date()
      #self.is_chunk()
		
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
    picture   = models.FileField(upload_to='gallery/%Y/%m/%d')
    caption   = models.CharField(_('caption'), max_length=255, blank=True)
    author    = models.CharField(_('author'), max_length=255, blank=True)
    sourceURL = models.URLField(_('source URL'), blank=True)
    picdate   = models.DateTimeField(_("pic date"))
    contractor = models.ForeignKey(Contractor, unique=True)

    def __str__(self):
        return self.author

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
