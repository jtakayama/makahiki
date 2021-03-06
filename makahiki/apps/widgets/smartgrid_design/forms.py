''' Forms for the Smart Grid Game Designer.

Created on Feb 5, 2013

@author: Cam Moore
'''

from django import forms
import ast
import datetime


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


class DeployToSmartgridForm(forms.Form):
    """Form for ensuring no cross-site for publishing the designer to the smartgrid."""
    use_filler = forms.BooleanField(required=False)


class DeleteLevelForm(forms.Form):
    """Form for ensuring no cross-site scripting for deleting a level in the designer."""
    level_slug = forms.CharField(max_length=25, help_text="Level slug", widget=forms.HiddenInput)


class DeleteDraftForm(forms.Form):
    """Form for deleting a draft in the designer."""
    draft_slug = forms.CharField(max_length=25, help_text="Draft slug", widget=forms.HiddenInput)


class EventDateForm(forms.Form):
    """Form for ensuring no cross-site scripting for setting event dates in the designer."""
    event_slug = forms.CharField(max_length=25, widget=forms.HiddenInput)
    event_date = forms.DateTimeField(initial=datetime.datetime.now)
    location = forms.CharField(max_length=40)


class AddLevelForm(forms.Form):
    """Form for adding a DesignerLevel. Ensures no cross-site scripting to create new levels."""
    level_name = forms.CharField(max_length=25, help_text="Level Name, must be unique.")
    unlock_condition = forms.CharField(max_length=40, help_text="Unlock Condition for the Level")


class NewDraftForm(forms.Form):
    """Form for adding a new Smart Grid Game Draft in the designer."""
    draft_name = forms.CharField(max_length=50, help_text="The name of the Draft Smart Grid Game")


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


class LoadTemplateForm(forms.Form):
    """Form for loading a template into a draft."""
    TYPE_CHOICES = (
        ('empty', 'Empty Grid'),
        ('demo', 'Demo'),
        ('default', 'Default'),
        ('uh12', 'KukuiCup/UH 12'),
        ('test', 'Test Grid'),
        )
    template = forms.ChoiceField(
        choices=TYPE_CHOICES,
        )
    draft_name = forms.CharField(max_length=50, help_text="The name of the Draft Smart Grid Game")
