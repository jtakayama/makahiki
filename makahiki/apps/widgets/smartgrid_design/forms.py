''' Forms for the Smart Grid Game Designer.

Created on Feb 5, 2013

@author: Cam Moore
'''

from django import forms
import ast


class ListFormField(forms.Field):
    """A form field that holds a python list."""
    def clean(self, value):
        return self.to_python(value)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)


class SggUpdateForm(forms.Form):
    """Form for holding the SGG updates."""
    category_updates = ListFormField(widget=forms.HiddenInput)
    action_updates = ListFormField(widget=forms.HiddenInput)


class RevertToSmartgridForm(forms.Form):
    """Form for ensuring no cross-site scripting for reverting designer."""
    pass


class DeployToSmartgridForm(forms.Form):
    """Form for ensuring no cross-site for publishing the designer to the smartgrid."""
    pass
