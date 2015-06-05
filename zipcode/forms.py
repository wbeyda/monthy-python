from django.forms import MultiWidget 
from django import forms
from zipcode.models import *

class SplitSelectDateTimeWidget(MultiWidget):
    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=None, years=None):
        widgets = (SelectDateWidget(attrs=attrs, years=years),\
                SelectTimeWidget(attrs=attrs,\
                    hour_step=hour_step,\
                   minute_step=minute_step, \
                   second_step=second_step, \
                   twelve_hr=twelve_hr\
                  ))
        super(SplitSelectDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

    def format_output(self, rendered_widgets):
        rendered_widgets.insert(-1, '<br/>')
        return u''.join(rendered_widgets)


class CareerForm(forms.ModelForm):
        class Meta:
            model = CareerResume

class ZipForm(forms.Form):
	zipsearch = forms.CharField(label='Enter your zipcode below to find the neighborhood hero in your area.', max_length=5)

class ContactForm(forms.Form):
	name = forms.CharField(label='Name', max_length=50)
	address = forms.CharField(label='Address', max_length=50)
	email = forms.EmailField(label='Email', max_length=50)
	problem = forms.CharField(widget=forms.Textarea, label='Description', max_length=200)

class CareerForm(forms.ModelForm):
        
        class Meta:
            model = CareerResume
 

class ContractorScheduleForm(forms.ModelForm):
        start_date = forms.SplitDateTimeWidget()
        end_date = forms.SplitDateTimeWidget()

        class Meta:
            model = ContractorSchedule
            #exclude = ('firstname')
