"""Prepares the rendering of Smart Grid Game widget."""


from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from apps.widgets.smartgrid_library.models import LibraryAction


def supply(request, page_name):
    """Supplies view_objects for smartgrid library widgets."""
    _ = page_name
    _ = request

    return {
        "levels": None,
        }


@never_cache
@login_required
def add_action(request, action_type, slug):
    """Handle the Submission of the task."""

    print "%s/%s" % (action_type, slug)
    return HttpResponseRedirect("/challenge_setting_admin/smartgrid_library/libraryaction/")


@never_cache
@login_required
def library_action_admin(request, pk):
    """handle the library action admin."""
    _ = request
    action = LibraryAction.objects.get(pk=pk)
    action_type = action.subtype if action.subtype != "excursion" else "event"

    return HttpResponseRedirect("/admin/smartgrid_library/library%s/%s/" % (action_type, pk))


@never_cache
@login_required
def library_action_admin_list(request):
    """handle the library action admin."""
    _ = request
    return HttpResponseRedirect("/admin/smartgrid_library/libraryaction/")
