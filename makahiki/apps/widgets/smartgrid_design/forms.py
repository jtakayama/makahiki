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


class RevertToSmartgridForm(forms.Form):
    """Form for ensuring no cross-site scripting for reverting designer."""
    pass


class DeployToSmartgridForm(forms.Form):
    """Form for ensuring no cross-site for publishing the designer to the smartgrid."""
    pass


class ExampleGridsForm(forms.Form):
    """Form for choosing between different example Smart Grid designs."""
    TYPE_CHOICES = (
        ('demo', 'Demo'),
        ('default', 'Default'),
        ('uh12', 'KukuiCup/UH 12'),
        ('test', 'Test Grid'),
        ('empty', 'Empty Grid'),
        )
    grid = forms.ChoiceField(
        choices=TYPE_CHOICES,
        )
