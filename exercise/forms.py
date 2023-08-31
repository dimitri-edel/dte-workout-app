"""Forms for the exercise app """
#pylint: disable=no-name-in-module
from django.forms import ModelForm
from .models import Exercise

class ExerciseForm(ModelForm):
    """Form for an exercise model"""
    class Meta:
        """Meta information"""
        model = Exercise
        fields = ["name", "exercise_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'input-field'        
        self.fields['name'].widget.attrs['placeholder'] = 'Name?'
        self.fields['exercise_type'].widget.attrs['class'] = 'input-field'
        