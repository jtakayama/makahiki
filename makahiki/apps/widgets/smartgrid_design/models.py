'''
Created on Feb 5, 2013

@author: Cam Moore
'''

from django.db import models
import ast


class ListField(models.TextField):
    """Represents a list as text. Can convert text string to python list."""
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value, None)


class Dummy(models.Model):
    """Dummy class has a ListField."""
    mylist = ListField()
