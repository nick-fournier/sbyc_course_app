from django import forms

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
    course_number = forms.IntegerField(label='Course Number')
    pin = forms.ChoiceField(choices=PIN)
    rounding = forms.ChoiceField(choices=ROUNDING)
    # custom_coords

    def foo(self):
        pass
