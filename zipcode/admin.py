from django.contrib.admin import AdminSite
from django.contrib import admin
from zipcode.models import *
from django.utils.translation import ugettext_lazy
AdminSite.site_header = "At Home Services Admin"
AdminSite.site_title = ugettext_lazy('At Home Services Site Admin')

class AvailabilityInline(admin.TabularInline):
    model = Availability


class ContractorAdmin(admin.ModelAdmin):
    inlines = [AvailabilityInline,]
    list_display = ('firstname', 'lastname','areacode', 'trade', 'secondaryTrades' ,'bio', 'pic',)
    fields = ('firstname', 'lastname', 'areacode', 'trade', 'secondaryTrades' ,'bio', 'pic',)
    prepopulated_fields = {"firstname": ("firstname",  'lastname',)}
    
class CareerResumeAdmin(admin.ModelAdmin):
    list_display = ('name','address','email','phone','resume')
    fields = ('name','address','email','phone','resume')
    prepopulated_fields = {"name": ("name",)}

class ContractorScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('firstname', 'title', 'start_date', 'end_date',( 'all_day', 'estimate', 'repair', 'maintenance', 'installation',),'background_color','description',)
        }),
        ('Location', {
            'classes': ('collapse',),
            'fields': ('location',)
        }),
    )

    list_display = ('id','firstname','title', 'start_date', 'end_date','all_day',)
    list_filter = ['id']
    search_fields = ['title']
    date_hierarchy = 'start_date'

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('author','picdate','picture','caption','sourceURL','contractor','job','testimonial','hashtags','socialtags')

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('approved_status',
                    'contractor',
                    'customer_name',
                    'customer_date',
                    'customer_city',
                    'customer_testimonial',
                    'job',
                    'image_tag',
                    'job_pic_url',
                    'hashtags',
                    'socialtags',
                    'best_of',)

    '''if User.is_staff:
        has_change_permission(best_of) = True
    else:
        has_change_permission(best_of) = False'''
    list_filter = ['customer_date','job']
    search_fields = ['job']
    readonly_fields = ('image_tag',)
    
    field_options = {
                    'fields': ('image_tag'),
                    'classes': ('extrapretty'),
                    }

    def mark_as_approved(self, request, queryset):
          rows_updated = queryset.update(approved_status = True)
          if rows_updated == 1:
              message_bit = "1 Testimonial was approved"
          else:
              message_bit = "%s Testimonials were approved" % rows_updated
          
          self.message_user(request, "%s successfully marked as approved." % message_bit)
    
    actions = [mark_as_approved]

class MonthlySpecialAdmin(admin.ModelAdmin):
    list_display = ('special_pic','special_text','special_color','special_active')
    exclude = ('special_url',)



admin.site.register(MonthlySpecial, MonthlySpecialAdmin)
#admin.site.register(Availability, AvailabilityInline)
admin.site.register(Contractor, ContractorAdmin)
admin.site.register(CareerResume, CareerResumeAdmin)
admin.site.register(ContractorSchedule, ContractorScheduleAdmin)
admin.site.register(Location)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
