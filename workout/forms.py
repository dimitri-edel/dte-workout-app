"""Forms used in the workout app """
#pylint: disable=no-name-in-module
#pylint: disable=too-few-public-methods
#pylint: disable=no-member
from django.forms import ModelForm, TextInput
from exercise.models import Exercise
from .models import Workout, WorkoutExercise


class WorkoutForm(ModelForm):
    """Form to harbor workout session objects"""
    class Meta:
        """"Meta information"""
        model = Workout
        fields = ["name"]

        labels = {
            'name' : ""
        }
        widgets = {
            'name': TextInput({'placeholder': 'Enter Name of Workout', 'class':'input-field col'}),
        }


class WorkoutExerciseForm(ModelForm):
    """Form that holds the data of the relationship WorkoutExercise"""

    class Meta:
        """"Meta information"""
        model= WorkoutExercise
        fields = ["exercise"]

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop("user_id")
        super(WorkoutExerciseForm, self).__init__(*args, **kwargs)        
        # Set the empty label in the selector
        self.fields['exercise'].empty_label = "( --- Select Exercise --- )"
        self.fields['exercise'].queryset = Exercise.objects.filter(owner=owner)
        self.fields['exercise'].widget.attrs.update({"class": "input-field"})
