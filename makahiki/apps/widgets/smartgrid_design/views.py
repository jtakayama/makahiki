"""Provides the view of the widget."""
from apps.widgets.smartgrid.models import Filler
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from apps.widgets.smartgrid import smartgrid
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from apps.widgets.smartgrid_design.forms import RevertToSmartgridForm, \
    DeployToSmartgridForm, ExampleGridsForm
from apps.widgets.smartgrid_library.models import LibraryActivity, LibraryEvent, \
    LibraryCommitment, LibraryColumnName
from apps.managers.smartgrid_mgr import smartgrid_mgr, unlock_lint
import json
from apps.widgets.smartgrid_design.models import DesignerLevel, DesignerColumnName, \
    DesignerAction, DesignerGrid, DesignerColumnGrid
from collections import OrderedDict


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    levels = DesignerLevel.objects.all()
    if len(levels) == 0:  # need to create default level
        l = DesignerLevel()
        l.name = "Level 1"  # no name
        l.slug = "default"
        l.unlock_condition = "True"
        l.unlock_condition_text = "Unlocked"
        l.save()

#    print smartgrid_mgr.get_designer_grid()
    return {
        'levels': levels,
        'columns': LibraryColumnName.objects.all(),
        'activities': LibraryActivity.objects.all(),
        'commitments': LibraryCommitment.objects.all(),
        'events': LibraryEvent.objects.all(),
        'fillers': Filler.objects.all(),
        'reset_form': RevertToSmartgridForm(),
        'publish_form': DeployToSmartgridForm(),
        'example_grid_form': ExampleGridsForm(),
        'palette': smartgrid_mgr.get_designer_palette(),
        'designer_grid': smartgrid_mgr.get_designer_grid(),
        'smart_grid_actions': smartgrid_mgr.get_designer_action_slugs(),
        'smart_grid_columns': smartgrid_mgr.get_designer_column_name_slugs(),
            }


@never_cache
@login_required
def designer_action_admin(request, pk):
    """handle the library action admin."""
    _ = request
    action = DesignerAction.objects.get(pk=pk)
    action_type = action.type

    return HttpResponseRedirect("/admin/smartgrid_design/designer%s/%s/" % (action_type, pk))


@never_cache
@login_required
def designer_action_admin_list(request):
    """handle the library action admin."""
    _ = request
    return HttpResponseRedirect("/admin/smartgrid_design/designeraction/")


@never_cache
@login_required
def view_action(request, action_type, slug):
    """individual action page"""
    _ = action_type
    action = smartgrid.get_action(slug=slug)
    user = request.user
    view_objects = {}

    action = smartgrid.annotate_action_details(user, action)

    return render_to_response("action.html", {
        "action": action,
        "display_form": True if "display_form" in request.GET else False,
        "view_objects": view_objects,
        }, context_instance=RequestContext(request))


def instantiate_column(request, col_slug, level_slug, column):
    """Instantiates the DesignerColumnName from the LibraryColumnName and places it in the
    Grid at the given level and column."""
    _ = request
    _ = level_slug
    lib_col = LibraryColumnName.objects.get(slug=col_slug)
    try:
        col_name = get_object_or_404(DesignerColumnName, slug=col_slug)
    except Http404:
        col_name = DesignerColumnName()

    col_name.name = lib_col.name
    col_name.slug = lib_col.slug
    col_name.save()

    level = get_object_or_404(DesignerLevel, slug=level_slug)
    grid = DesignerColumnGrid()
    grid.level = level
    grid.column = column
    grid.name = col_name
    grid.save()

    #  Return the new pk for the instantiated DesignerColumnName.
    return HttpResponse(json.dumps({
            "pk": col_name.pk,
            }), mimetype="application/json")


def instantiate_action(request, action_slug, level_slug, column, row):
    """Instantiated the Smart Grid Game Action from the Library Action with the
    given level, column, and row."""
    _ = request
    grid_action = smartgrid_mgr.instantiate_designer_from_library(action_slug)
    level = DesignerLevel.objects.get(slug=level_slug)
    grid = DesignerGrid()
    grid.level = level
    grid.column = column
    grid.row = row
    grid.action = grid_action
    grid.save()

    #  Return the new pk for the instantiated action.
    return HttpResponse(json.dumps({
            "pk": grid_action.pk,
            }), mimetype="application/json")


def move_action(request, action_slug, level_slug, old_column, old_row, new_column, new_row):
    """Moves the Designer Grid Action from the old column and row to the new column and row."""
    _ = request
    _ = level_slug

    action = smartgrid_mgr.get_designer_action(action_slug)
    for grid in DesignerGrid.objects.filter(action=action):
        if grid.column == int(old_column) and grid.row == int(old_row):
            grid.column = new_column
            grid.row = new_row
            grid.save()

    #  Return the pk for the moved action.
    return HttpResponse(json.dumps({
            "pk": action.pk,
            }), mimetype="application/json")


def move_palette_action(request, action_slug, level_slug, new_column, new_row):
    """Moves the Designer Grid Action from the palette to the new column and row."""
    _ = request

    action = smartgrid_mgr.get_designer_action(action_slug)
    level = DesignerLevel.objects.get(slug=level_slug)
    grid = DesignerGrid()
    grid.level = level
    grid.column = new_column
    grid.row = new_row
    grid.action = action
    grid.save()

    #  Return the pk for the moved action.
    return HttpResponse(json.dumps({
            "pk": action.pk,
            }), mimetype="application/json")


def delete_action(request, action_slug):
    """Deletes the given Smart Grid Game Action."""
    _ = request
    action = smartgrid.get_action(action_slug)
    action.delete()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def delete_column(request, col_slug):
    """Deletes the DesignerColumnName for the given col_slug."""
    _ = request
    column = get_object_or_404(DesignerColumnName, slug=col_slug)
    column.delete()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def clear_from_grid(request, action_slug):
    """Removes the DesignerAction for the given action_slug from the DesignerGrid."""
    _ = request
    action = smartgrid_mgr.get_designer_action(action_slug)
    for grid in DesignerGrid.objects.filter(action=action):
        print grid
        grid.delete()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def revert_to_grid(request):
    """Deletes all the DesignerActions and creates new DesignerActions from the current Smart
    Grid Game instances."""
    if request.method == 'POST':  # If the form has been submitted...
        form = RevertToSmartgridForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            smartgrid_mgr.clear_designer()
            smartgrid_mgr.copy_smartgrid_to_designer()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def publish_to_grid(request):
    """Clears all the current Smart Grid Instances and Copies the DesignerActions to the Smart
    Grid Game."""
    if request.method == 'POST':
        form = DeployToSmartgridForm(request.POST)
        if form.is_valid():
            use_filler = form.cleaned_data['use_filler']
            smartgrid_mgr.deploy_designer_to_smartgrid(use_filler)
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def load_example_grid(request):
    """Clears the Designer and loads the example grid with the given name."""
    if request.method == 'POST':
        form = ExampleGridsForm(request.POST)
        if form.is_valid():
            example_name = form.cleaned_data['grid']
            if example_name == 'empty':
                smartgrid_mgr.clear_designer()
            else:
                smartgrid_mgr.load_example_grid(example_name)
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def run_lint(request):
    """Runs unlock_lint over the DesignerActions and shows the results in a page."""
    _ = request
    trees = unlock_lint.build_designer_trees()
    sorted_trees = OrderedDict(sorted(trees.items(), key=lambda t: -len(t[1])))
    unlock_tree = ''
    for k in list(sorted_trees):
        unlock_tree += sorted_trees[k].tohtmlstring()
        unlock_tree += '<p></p>'
    unreachable = unlock_lint.get_unreachable_designer_actions()
    false_unlock = unlock_lint.get_false_unlock_designer_actions()
    mismatched_levels = unlock_lint.get_missmatched_designer_level()
    return HttpResponse(json.dumps({
            "tree": unlock_tree,
            "unreachable": unreachable,
            "false_unlock": false_unlock,
            "mismatched_levels": mismatched_levels,
            }), mimetype="application/json")


def get_diff(request):
    """Returns the difference between the designer grid and the Smart Grid as a string."""
    _ = request
    diff = smartgrid_mgr.diff_between_designer_and_grid()
    return HttpResponse(json.dumps({
            "diff": diff,
            }), mimetype="application/json")
