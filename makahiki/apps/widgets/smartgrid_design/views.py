"""Provides the view of the widget."""
from apps.widgets.smartgrid.models import Filler
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from apps.widgets.smartgrid import smartgrid
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from apps.widgets.smartgrid_design.forms import RevertToSmartgridForm, \
    DeployToSmartgridForm, ExampleGridsForm, DeleteLevelForm, AddLevelForm, EventDateForm,\
    NewDraftForm, LoadTemplateForm
from apps.widgets.smartgrid_library.models import LibraryActivity, LibraryEvent, \
    LibraryCommitment, LibraryColumnName
from apps.managers.smartgrid_mgr import smartgrid_mgr, unlock_lint
import json
from apps.widgets.smartgrid_design.models import DesignerLevel, \
    DesignerAction, DesignerGrid, DesignerColumnGrid, Draft
from collections import OrderedDict
from django.template.defaultfilters import slugify
from apps.utils import utils


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    draft_choices = Draft.objects.all()
    draft = None
    levels = []
    if len(draft_choices) != 0:
        try:
            draft_slug = request.REQUEST['draft']
        except KeyError:
            draft_slug = draft_choices[0].slug
        try:
            draft = smartgrid_mgr.get_designer_draft(draft_slug)
        except Http404:
            draft = smartgrid_mgr.get_designer_draft('default')
        levels = DesignerLevel.objects.filter(draft=draft)
        if len(levels) == 0:  # need to create default level
            l = DesignerLevel()
            l.name = "Level 1"  # no name
            l.slug = "default"
            l.unlock_condition = "True"
            l.unlock_condition_text = "Unlocked"
            l.draft = draft
            l.save()
        levels = DesignerLevel.objects.filter(draft=draft)

    return {
        'draft': draft,
        'draft_choices': draft_choices,
        'levels': levels,
        'columns': LibraryColumnName.objects.all(),
        'activities': LibraryActivity.objects.all(),
        'commitments': LibraryCommitment.objects.all(),
        'events': LibraryEvent.objects.all(),
        'fillers': Filler.objects.all(),
        'reset_form': RevertToSmartgridForm(),
        'publish_form': DeployToSmartgridForm(),
        'example_grid_form': ExampleGridsForm(),
        'add_level_form': AddLevelForm(),
        'delete_level_form': DeleteLevelForm(),
        'event_date_form': EventDateForm(),
        'new_draft_form': NewDraftForm(),
        'load_template_form': LoadTemplateForm(),
        'palette': smartgrid_mgr.get_designer_palette(draft),
        'designer_grid': smartgrid_mgr.get_designer_grid(draft),
        'designer_actions': smartgrid_mgr.get_designer_action_slugs(draft),
        'designer_columns': smartgrid_mgr.get_designer_column_name_slugs(draft),
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


def instantiate_column(request, col_slug, level_slug, column, draft_slug):
    """Instantiates the DesignerColumnName from the LibraryColumnName and places it in the
    Grid at the given level and column."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    col = smartgrid_mgr.instantiate_designer_column_from_library(draft, col_slug)

    level = smartgrid_mgr.get_designer_level(draft, level_slug)
    grid = DesignerColumnGrid()
    grid.level = level
    grid.column = column
    grid.name = col
    grid.draft = draft
    grid.save()

    #  Return the new pk for the instantiated DesignerColumnName.
    return HttpResponse(json.dumps({
            "pk": col.pk,
            }), mimetype="application/json")


def instantiate_action(request, action_slug, level_slug, column, row, draft_slug):
    """Instantiated the Smart Grid Game Action from the Library Action with the
    given level, column, and row."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    grid_action = smartgrid_mgr.instantiate_designer_action_from_library(draft, action_slug)
    level = smartgrid_mgr.get_designer_level(draft, level_slug)
    grid = DesignerGrid()
    grid.level = level
    grid.column = column
    grid.row = row
    grid.action = grid_action
    grid.draft = draft
    grid.save()

    #  Return the new pk for the instantiated action.
    return HttpResponse(json.dumps({
            "pk": grid_action.pk,
            }), mimetype="application/json")


def copy_action(request, action_slug, draft_slug):
    """Copies the given DesignerAction into the palette for the given draft."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    smartgrid_mgr.copy_designer_action(draft, action_slug)
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def move_action(request, action_slug, level_slug, old_column, old_row, new_column, new_row, \
                draft_slug):
    """Moves the Designer Grid Action from the old column and row to the new column and row."""
    _ = request
    _ = level_slug
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    action = smartgrid_mgr.get_designer_action(draft, action_slug)
    level = smartgrid_mgr.get_designer_level(draft, level_slug)
    for grid in DesignerGrid.objects.filter(draft=draft, action=action, level=level):
        if grid.column == int(old_column) and grid.row == int(old_row):
            grid.column = new_column
            grid.row = new_row
            grid.save()

    #  Return the pk for the moved action.
    return HttpResponse(json.dumps({
            "pk": action.pk,
            }), mimetype="application/json")


def move_palette_action(request, action_slug, level_slug, new_column, new_row, draft_slug):
    """Moves the Designer Grid Action from the palette to the new column and row."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    action = smartgrid_mgr.get_designer_action(draft, action_slug)
    level = smartgrid_mgr.get_designer_level(draft, level_slug)
    grid = DesignerGrid()
    grid.level = level
    grid.column = new_column
    grid.row = new_row
    grid.action = action
    grid.draft = draft
    grid.save()

    #  Return the pk for the moved action.
    return HttpResponse(json.dumps({
            "pk": action.pk,
            }), mimetype="application/json")


def delete_action(request, action_slug, draft_slug):
    """Deletes the given Smart Grid Game Action."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    action = smartgrid_mgr.get_designer_action(draft, action_slug)
    action.delete()
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def delete_column(request, col_slug, draft_slug):
    """Deletes the DesignerColumnName for the given col_slug."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    column = smartgrid_mgr.get_designer_column_name(draft, col_slug)
    column.delete()
    response = HttpResponse("/sgg_designer/?draft=%s" % draft.slug)
    return response


def clear_from_grid(request, action_slug, draft_slug):
    """Removes the DesignerAction for the given action_slug from the DesignerGrid."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    action = smartgrid_mgr.get_designer_action(draft, action_slug)
    for grid in DesignerGrid.objects.filter(draft=draft, action=action):
        grid.delete()
    response = HttpResponse("/sgg_designer/?draft=%s" % draft.slug)
    return response


def revert_to_grid(request, draft_slug):
    """Deletes all the DesignerActions and creates new DesignerActions from the current Smart
    Grid Game instances."""
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    if request.method == 'POST':  # If the form has been submitted...
        form = RevertToSmartgridForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            smartgrid_mgr.clear_designer(draft)
            smartgrid_mgr.copy_smartgrid_to_designer(draft)
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def publish_to_grid(request, draft_slug):
    """Clears all the current Smart Grid Instances and Copies the DesignerActions to the Smart
    Grid Game."""
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    if request.method == 'POST':
        form = DeployToSmartgridForm(request.POST)
        if form.is_valid():
            use_filler = form.cleaned_data['use_filler']
            smartgrid_mgr.deploy_designer_to_smartgrid(draft, use_filler)
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def load_example_grid(request, draft_slug):
    """Clears the Designer and loads the example grid with the given name."""
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    if request.method == 'POST':
        form = ExampleGridsForm(request.POST)
        if form.is_valid():
            example_name = form.cleaned_data['grid']
            if example_name == 'empty':
                smartgrid_mgr.clear_designer(draft)
            else:
                smartgrid_mgr.load_example_grid(draft, example_name)
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def load_template(request):
    """Loads a template into the given draft."""
    if request.method == 'POST':
        form = LoadTemplateForm(request.POST)
        if form.is_valid():
            draft_name = form.cleaned_data['draft_name']
            template_name = form.cleaned_data['template']
            draft_slug = slugify(draft_name)
            try:
                draft = smartgrid_mgr.get_designer_draft(draft_slug)
            except Http404:
                draft = Draft(name=draft_name, slug=draft_slug)
                draft.save()
            smartgrid_mgr.clear_designer(draft)
            if template_name != 'empty':
                smartgrid_mgr.clear_designer(draft=None)
                smartgrid_mgr.load_example_grid(draft, template_name)
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def run_lint(request, draft_slug):
    """Runs unlock_lint over the DesignerActions and shows the results in a page."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    trees = unlock_lint.build_designer_trees(draft)
    sorted_trees = OrderedDict(sorted(trees.items(), key=lambda t: -len(t[1])))
    unlock_tree = ''
    for k in list(sorted_trees):
        unlock_tree += sorted_trees[k].tohtmlstring()
        unlock_tree += '<p></p>'
    unreachable = unlock_lint.get_unreachable_designer_actions(draft)
    false_unlock = unlock_lint.get_false_unlock_designer_actions(draft)
    mismatched_levels = unlock_lint.get_missmatched_designer_level(draft)
    return HttpResponse(json.dumps({
            "tree": unlock_tree,
            "unreachable": unreachable,
            "false_unlock": false_unlock,
            "mismatched_levels": mismatched_levels,
            "pub_date": unlock_lint.check_pub_exp_dates(draft),
            }), mimetype="application/json")


def get_diff(request, draft_slug):
    """Returns the difference between the designer grid and the Smart Grid as a string."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    diff = smartgrid_mgr.diff_between_designer_and_grid(draft)
    return HttpResponse(json.dumps({
            "diff": diff,
            }), mimetype="application/json")


def delete_level(request, draft_slug):
    """Deletes the DesignerLevel for the given level_slug and removes all the location
    information for the level."""
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    if request.method == 'POST':
        form = DeleteLevelForm(request.POST)
        if form.is_valid():
            level_slug = form.cleaned_data['level_slug']
            level = smartgrid_mgr.get_designer_level(draft, slug=level_slug)
            for grid in DesignerColumnGrid.objects.filter(draft=draft, level=level):
                grid.delete()
            for grid in DesignerGrid.objects.filter(draft=draft, level=level):
                grid.delete()
            level.delete()
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def add_level(request, draft_slug):
    """Creates a new level."""
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    if request.method == 'POST':
        form = AddLevelForm(request.POST)
        if form.is_valid():
            max_priority = 0
            for level in DesignerLevel.objects.filter(draft=draft):
                if max_priority < level.priority:
                    max_priority = level.priority
            max_priority += 1
            slug = slugify(form.cleaned_data['level_name'])
            level = DesignerLevel(name=form.cleaned_data['level_name'], slug=slug, \
                                  priority=max_priority, draft=draft)
            predicate = form.cleaned_data['unlock_condition']
            if not utils.validate_predicates(predicate):
                level.unlock_condition = predicate
            else:
                level.unlock_condition = 'False'  # What is the correct default value?
            level.save()
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def set_event_date(request, draft_slug):
    """Sets the event date from the EventDateForm."""
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    if request.method == 'POST':
        form = EventDateForm(request.POST)
        if form.is_valid():
            event_slug = form.cleaned_data['event_slug']
            event = smartgrid_mgr.get_designer_action(draft=draft, slug=event_slug)
            event_date = form.cleaned_data['event_date']
            event.event_date = event_date
            event.event_location = form.cleaned_data['location']
            event.save()
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def new_draft(request):
    """Creates a new Draft from the given draft name if the Draft doesn't already exist."""
    if request.method == 'POST':
        form = NewDraftForm(request.POST)
        if form.is_valid():
            draft_name = form.cleaned_data['draft_name']
            draft_slug = slugify(draft_name)
            try:
                draft = smartgrid_mgr.get_designer_draft(draft_slug)
            except Http404:
                draft = Draft(name=draft_name, slug=draft_slug)
                draft.save()
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response
