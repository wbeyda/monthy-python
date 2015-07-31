from django.forms import MultiWidget
from django.forms import SplitDateTimeField  
from django import forms
from zipcode.models import *
        
class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerResume
        fields = ['name', 'address', 'email', 'phone', 'resume']

class ZipForm(forms.Form):
    zipsearch = forms.CharField(label='Zipcode', max_length=5)

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    address = forms.CharField(label='Address', max_length=50)
    email = forms.EmailField(label='Email', max_length=50)
    problem = forms.CharField(widget=forms.Textarea, label='Description', max_length=200)


class ContractorScheduleForm(forms.ModelForm):
		start_date = SplitDateTimeField()
		end_date   = SplitDateTimeField()
		
		class Meta:
                        model = ContractorSchedule
                        fields = ['firstname', 'start_date','end_date', 'all_day', 'title', 'description', 'location', 'background_color']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['customer_name','customer_city','customer_testimonial','job','job_pic','job_pic_url','hashtags','socialtags']

def testimonialform_factory(qs):

    class TestimonialForm(forms.ModelForm):
        job = forms.ModelMultipleChoiceField(queryset=qs)
        class Meta:
            model = Testimonial
            fields =     ['customer_name','customer_city','customer_testimonial','job','job_pic','job_pic_url','hashtags','socialtags']
            exclude = ['best_of']    
    return TestimonialForm

