from django.contrib.admin import AdminSite
from django.contrib import admin
from zipcode.models import *
from django.utils.translation import ugettext_lazy
AdminSite.site_header = "AHS Admin"
AdminSite.site_title = ugettext_lazy('AHS Site Admin')

class ContractorAdmin(admin.ModelAdmin):
	list_display = ('firstname', 'lastname','areacode', 'trade', 'secondaryTrades' ,'bio', 'pic')
	fields = ('firstname', 'lastname', 'areacode', 'trade', 'secondaryTrades' ,'bio', 'pic')
	prepopulated_fields = {"firstname": ("firstname",  'lastname',)}

class CareerResumeAdmin(admin.ModelAdmin):
    list_display = ('name','address','email','phone','resume')
    fields = ('name','address','email','phone','resume')
    prepopulated_fields = {"name": ("name",)}

class ContractorScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('firstname', 'start_date', 'end_date', 'title', 'background_color','description',)
        }),
        ('Location', {
            'classes': ('collapse',),
            'fields': ('location',)
        }),
    )

    list_display = ('firstname','title', 'start_date', 'end_date',)
    list_filter = ['start_date']
    search_fields = ['title']
    date_hierarchy = 'start_date'

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('author','picdate','picture','caption','sourceURL',)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('approved_status','contractor','customer_name','customer_date','customer_city','customer_testimonial','job','job_pic','job_pic_url','hashtags','socialtags',)
    list_filter = ['customer_date','job']
    search_fields = ['job']



admin.site.register(Contractor, ContractorAdmin)
admin.site.register(CareerResume, CareerResumeAdmin)
admin.site.register(ContractorSchedule, ContractorScheduleAdmin)
admin.site.register(Location)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
