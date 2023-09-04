"""Form for Workload"""
#pylint: disable=no-name-in-module
#pylint: disable=too-few-public-methods
from django.forms import ModelForm
from .models import Workload

class WorkloadForm(ModelForm):
    """Form for serializing the fields of Workload"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reps'].widget.attrs['class'] = 'input-field'
        self.fields['weight'].widget.attrs['class'] = 'input-field'
        self.fields['time'].widget.attrs['class'] = 'input-field'
        self.fields['distance'].widget.attrs['class'] = 'input-field'


    class Meta:
        """Meta information for the workload"""
        model = Workload
        fields = ["reps","weight", "time","distance"]
