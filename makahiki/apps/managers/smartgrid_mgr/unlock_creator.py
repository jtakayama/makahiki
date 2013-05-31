'''Helps the Smartgrid Designer build correct unlock_conditions by allowing them to choose from
valid choices not just type into the unlock_codition text field.
Created on May 30, 2013

@author: Cam Moore
'''
from apps.widgets.smartgrid_library.models import LibraryAction
from apps.widgets.smartgrid_design.models import DesignerAction


# Used to build the unlock_conditions
(_AND, _OR, _NOT, _TRUE, _FALSE) = ('and', 'or', 'not', 'True', 'False')


def __get_library_action_slugs():
    """Returns a list of the LibraryAction slugs."""
    ret = []
    for action in LibraryAction.objects.all():
        if action.slug not in ret:
            ret.append(action.slug)
    return ret


def __get_action_slugs(draft):
    """Returns a list of all the slugs available in the given draft.  This includes all the
    LibraryAction slugs and any new action slugs in the draft."""
    ret = __get_library_action_slugs()
    for action in DesignerAction.objects.filter(draft=draft):
        if action.slug not in ret:
            ret.append(action.slug)
    return ret
