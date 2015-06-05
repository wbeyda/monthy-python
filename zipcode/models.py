from django.db import models
from django.utils.translation import ugettext_lazy as _

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

class ContractorSchedule(models.Model):
    firstname = models.ForeignKey(Contractor)
    start_date = models.DateTimeField(verbose_name=_("start date"))
    end_date = models.DateTimeField(_("end date"))
    all_day = models.BooleanField(_("all day"), default=False)
    title = models.CharField(_("title"), max_length=255, blank=True)
    description = models.TextField(_("description"),blank=True)
    location = models.ManyToManyField(
        'Location', verbose_name=_('locations'), blank=True
    )

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

class Testimonials(models.Model):
    customer_name        = models.CharField(_('customer name'), max_length=255, blank=True)
    customer_city        = models.CharField(_('customer city'), max_length=255, blank=True)
    customer_testimonial = models.TextField(_('customer testimonial'), max_length=255, blank=True)
    customer_date        = models.DateTimeField(_("customer date"))
