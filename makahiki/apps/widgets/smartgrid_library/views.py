"""Prepares the rendering of Smart Grid Game widget."""


from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from apps.widgets.smartgrid_library.models import LibraryAction
from apps.managers.smartgrid_mgr import smartgrid_mgr


def supply(request, page_name):
    """Supplies view_objects for smartgrid library widgets."""
    _ = page_name
    _ = request

    return {
        "levels": None,
        }


@never_cache
@login_required
def library_action_admin(request, pk):
    """handle the library action admin."""
    _ = request
    action = LibraryAction.objects.get(pk=pk)
    action_type = action.type

    return HttpResponseRedirect("/admin/smartgrid_library/library%s/%s/" % (action_type, pk))


@never_cache
@login_required
def library_action_admin_list(request):
    """handle the library action admin."""
    _ = request
    return HttpResponseRedirect("/admin/smartgrid_library/libraryaction/")


def copy_action(request, action_slug, draft_slug):
    """Copies the LibraryAction for the given action_slug."""
    _ = request
    smartgrid_mgr.copy_library_action(action_slug)
    response = HttpResponse("/sgg_designer/?draft=%s" % draft_slug)
    return response
