from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
import yaml
import os

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(THIS_PATH, 'fixtures/map_data/course_order.yaml')) as f:
    courses = yaml.load(f, Loader=yaml.FullLoader)

COURSES = (
    ('', 'Select course...'),
    *tuple([(c['course_number'], 'Course #' + str(c['course_number'])) for c in courses])
)

PIN = (
    # ('', 'Select start pin...'),
    ('RC BOAT', 'Race Committee Boat'),
    ('T1', 'T1 (Orange buoy)'),
)
ROUNDING = (
    # ('', 'Select windward rounding...'),
    ('PORT', 'Port rounding (red flag)'),
    ('STARBOARD', 'Starboard rounding (green flag)')
)

class CourseForm(forms.Form):
    course_number = forms.ChoiceField(choices=COURSES, initial="Course Number")
    # pin = forms.ChoiceField(choices=PIN, initial='RC BOAT')'
    rounding = forms.ChoiceField(choices=ROUNDING)
    # custom_coords

    def __init__(self, *args, **kwargs):
        url_kwargs = kwargs.pop('url_kwargs')
        kwargs.update(initial=url_kwargs)
        super(CourseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
        Div(
            Field('course_number', wrapper_class='col-md-3', onchange="this.form.submit()"),
            Field('rounding', wrapper_class='col-md-3', onchange="this.form.submit()"),
            # Field('pin', wrapper_class='col-md-3', onchange="this.form.submit()"),  
        css_class='form-row') 
    )
