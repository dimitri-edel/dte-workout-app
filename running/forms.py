"""Form for Workload"""
#pylint: disable=no-name-in-module
#pylint: disable=too-few-public-methods
from django.forms import ModelForm
from .models import Running


class RunningForm(ModelForm):
    """Form for serializing the fields of Workload"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].widget.attrs['class'] = 'input-field'
        self.fields['distance'].widget.attrs['class'] = 'input-field'        

    class Meta:
        """Meta information for the workload"""
        model = Running
        fields = ["time","distance"]
