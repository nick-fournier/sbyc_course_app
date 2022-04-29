from django import forms

class NameForm(forms.Form):
    course_number = forms.CharField(label='Course Number', max_length=100)
    # pin
    # rounding
    # custom_coords
