'''
Created on May 25, 2013

@author: Cam Moore
'''
from django.forms import ModelForm
from apps.managers.smartgrid_mgr.models import GccSettings


class GccSettingsForm(ModelForm):
    """Form for editing the GccSettings."""
    class Meta:
        """meta."""
        model = GccSettings
        exclude = ('user', )
