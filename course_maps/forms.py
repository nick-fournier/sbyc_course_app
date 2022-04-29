from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

PIN = (
    # ('', 'Choose...'),
    ('T1', 'T1 (Orange buoy)'),
    ('RC BOAT', 'Race Committee Boat')
)
ROUNDING = (
    # ('', 'Choose...'),
    ('PORT', 'Port'),
    ('STARBOARD', 'Starboard')
)

class CourseForm(forms.Form):
    course_number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Course Number'}))
    pin = forms.ChoiceField(choices=PIN)
    rounding = forms.ChoiceField(choices=ROUNDING)
    # custom_coords

    def __init__(self, *args, **kwargs):
        url_kwargs = kwargs.pop('url_kwargs')
        kwargs.update(initial=url_kwargs)
        print(kwargs)
        super(CourseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('course_number', css_class='form-group col-md-2 mb-0'),
                Column('pin', css_class='form-group col-md-3 mb-0'),
                Column('rounding', css_class='form-group col-md-3 mb-0'),
                Submit('submit', 'Update'),
                css_class='form-row'
            )
        )

