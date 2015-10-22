from django.contrib.admin import AdminSite
from django.contrib import admin
from zipcode.models import *
from django.utils.translation import ugettext_lazy
from image_cropping import ImageCroppingMixin
AdminSite.site_header = "At Home Services Admin"
AdminSite.site_title = ugettext_lazy('At Home Services Site Admin')

class AvailabilityInline(admin.TabularInline):
    model = Availability


class ContractorAdmin(ImageCroppingMixin, admin.ModelAdmin):
    inlines = [AvailabilityInline,]
    list_display = ('user','firstname', 'lastname','areacode', 'trade', 'secondaryTrades' ,'bio', 'image_tag',)
    #fields = ('firstname', 'lastname', 'areacode', 'trade', 'secondaryTrades' ,'bio', 'pic',)
    #prepopulated_fields = {"firstname": ("firstname",  'lastname',)}
    #readonly_fields = ('image_tag',)
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ( 'customerName' , 'email', 'phone_number', 'address_line_1', 'address_line_2', 'city', 'state', 'zipcode', 'subscribed',)

    def customerName(self, obj):
        return obj.last_name + ', ' + obj.first_name
    
    customerName.short_description = 'Customer Name'


class CareerResumeAdmin(admin.ModelAdmin):
    list_display = ('name','address','email','phone','resume')
    fields = ('name','address','email','phone','resume')
    prepopulated_fields = {"name": ("name",)}

class ContractorScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('firstname', 'customer', 'title', 'start_date', 'end_date',( 'all_day', 'estimate', 'repair', 'maintenance', 'installation',),'description',)
        }),
        ('Location', {
            'classes': ('collapse',),
            'fields': ('location',)
        }),
    )

    list_display = ('id','firstname','getCustomerName', 'title', 'start_date', 'end_date','all_day',  'approved', 'pending', 'completed')
    list_filter = ['id']
    list_display_links = ('firstname',)
    search_fields = ['title']
    date_hierarchy = 'start_date'
    
    def getCustomerName(self,obj):
        return obj.customer.first_name + ', ' + obj.customer.last_name
    getCustomerName.short_description = "Customer Name"
    
    def get_queryset(self, request):
        qs = super(ContractorScheduleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(firstname__user__username = request.user.username)



class GalleryAdmin(admin.ModelAdmin):
    list_display = ('author','picdate','picture','caption','sourceURL','contractor','job','testimonial','hashtags','socialtags')

    def get_queryset(self, request):
        qs = super(GalleryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(contractor__user__username = request.user.username)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('approved_status',
                    'contractor',
                    'customer',
                    'customer_date',
                    'truncate_words',
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

    def truncate_words(self, obj, length=350, suffix="..."):
        if len(obj.customer_testimonial) <= length:
            return obj.customer_testimonial
        else:
            return ' '.join(obj.customer_testimonial[:length].split(' ')[0:-1]) + suffix
    truncate_words.short_description = 'Customer Testimonial'        

    def mark_as_approved(self, request, queryset):
          rows_updated = queryset.update(approved_status = True)
          if rows_updated == 1:
              message_bit = "1 Testimonial was approved"
          else:
              message_bit = "%s Testimonials were approved" % rows_updated
          
          self.message_user(request, "%s successfully marked as approved." % message_bit)
    
    actions = [mark_as_approved]

    def get_queryset(self, request):
        qs = super(TestimonialAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(contractor__user__username = request.user.username)


class MonthlySpecialAdmin(admin.ModelAdmin):
    list_display = ('image_tag','special_pic', 'special_text','special_color','special_active')
    exclude = ('special_url',)



admin.site.register(MonthlySpecial, MonthlySpecialAdmin)
#admin.site.register(Availability, AvailabilityInline)
admin.site.register(Contractor, ContractorAdmin)
admin.site.register(CareerResume, CareerResumeAdmin)
admin.site.register(ContractorSchedule, ContractorScheduleAdmin)
admin.site.register(Location)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
