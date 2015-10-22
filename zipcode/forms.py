from django.forms import MultiWidget
from django.forms import SplitDateTimeField  
from django.forms import CharField 
from django.forms.widgets import TextInput
from django.forms.widgets import HiddenInput 
from django import forms
from zipcode.models import *
        
class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerResume
        fields = ['name', 'address', 'email', 'phone', 'resume']
        labels = {'name': 'Name', 'address': 'Address', 'email': 'E-Mail', 'phone': 'Phone Number', 'resume': 'Resume'}

class ZipForm(forms.Form):
    zipsearch = forms.CharField(label='Zipcode', max_length=5)

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    address = forms.CharField(label='Address', max_length=50)
    email = forms.EmailField(label='Email', max_length=50)
    problem = forms.CharField(widget=forms.Textarea, label='Description', max_length=200)


class ContractorScheduleForm(forms.ModelForm):

    class Meta:
        model = ContractorSchedule
        fields = ['firstname','customer', 'start_date','end_date', 'all_day', 'repair', 'estimate', 'installation', 'maintenance', 'value_care', 'emergency', 'description', 'location',]
        labels = {'customer': 'Phone'}
        widgets = {
                    'customer': TextInput( attrs= {'required': True, 'placeholder': '801-486-4418'}),
                    'firstname': HiddenInput(),
                  }
        
    def __init__(self, *args, **kwargs):
        super(ContractorScheduleForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = SplitDateTimeField()
        self.fields['end_date'] = SplitDateTimeField()


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['customer','customer_testimonial','job','job_pic','job_pic_url','hashtags','socialtags']
    

def testimonialform_factory(qs):

    class TestimonialForm(forms.ModelForm):
        job = forms.ModelMultipleChoiceField(queryset=qs)
        class Meta:
            model = Testimonial
            fields =     ['customer','customer_testimonial','job','job_pic','job_pic_url','hashtags','socialtags']
            labels = {'customer': 'Phone'}
            widgets = {
                        'customer': TextInput( attrs= {'required': True, 'placeholder': '801-486-4418'}),
                        'best_of': HiddenInput(),
                      }


    return TestimonialForm


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address_line_1', 'address_line_2', 'city', 'state', 'zipcode', 'subscribed'] 
        exclude = ['special_notes']





