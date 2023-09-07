"""Form for Workload"""
#pylint: disable=no-name-in-module
#pylint: disable=too-few-public-methods
from django.forms import ModelForm
from .models import Endurance


class EnduranceForm(ModelForm):
    """Form for serializing the fields of Workload"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reps'].widget.attrs['class'] = 'input-field'
        self.fields['time'].widget.attrs['class'] = 'input-field'        

    class Meta:
        """Meta information for the workload"""
        model = Endurance
        fields = ["reps","time"]
