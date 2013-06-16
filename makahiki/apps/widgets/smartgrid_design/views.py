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
    NewDraftForm, LoadTemplateForm, DeleteDraftForm
from apps.widgets.smartgrid_library.models import LibraryActivity, LibraryEvent, \
    LibraryCommitment, LibraryColumnName
from apps.managers.smartgrid_mgr import smartgrid_mgr, gcc, action_dependency
import json
from apps.widgets.smartgrid_design.models import DesignerLevel, \
    DesignerAction, DesignerGrid, DesignerColumnGrid, Draft
from django.template.defaultfilters import slugify
from apps.managers.smartgrid_mgr.forms import GccSettingsForm
from apps.managers.smartgrid_mgr.models import GccSettings
from apps.managers.smartgrid_mgr.gcc_model import _ERRORS, _WARNINGS
from django.utils import importlib
from apps.managers.predicate_mgr import predicate_mgr


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = page_name
    user = request.user
    gcc_settings, _ = GccSettings.objects.get_or_create(user=user)
    draft_choices = Draft.objects.all()
    draft = None
    tree_list = None
    levels = []
    if len(draft_choices) != 0:
        try:
            draft_slug = request.REQUEST['draft']
        except KeyError:
            try:
                draft_slug = request.COOKIES['current-designer-draft']
            except KeyError:
                draft_slug = draft_choices[0].slug
        try:
            draft = smartgrid_mgr.get_designer_draft(draft_slug)
        except Http404:
            draft = draft_choices[0]
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
        ts = action_dependency.build_designer_grid_trees(draft)
        tree_list = []
        for k in  list(ts):
            tree_list.append(ts[k].tohtmlstring())
    results = gcc.run_designer_checks(draft, gcc_settings)

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
        'delete_draft_form': DeleteDraftForm(),
        'load_template_form': LoadTemplateForm(),
        'gcc_settings_form': GccSettingsForm(instance=gcc_settings),
        'palette': smartgrid_mgr.get_designer_palette(draft),
        'designer_grid': smartgrid_mgr.get_designer_grid(draft),
        'designer_actions': smartgrid_mgr.get_designer_action_slugs(draft),
        'designer_columns': smartgrid_mgr.get_designer_column_name_slugs(draft),
        'errors': results[_ERRORS],
        'warnings': results[_WARNINGS],
        'trees': tree_list,
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
    grid, _ = DesignerColumnGrid.objects.get_or_create(draft=draft, name=col, level=level)
    grid.column = column
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


def delete_draft(request):
    """Deletes the Draft in the DeleteDraftForm."""
    if request.method == 'POST':
        form = DeleteDraftForm(request.POST)
        if form.is_valid():
            draft_slug = form.cleaned_data['draft_slug']
            draft = smartgrid_mgr.get_designer_draft(draft_slug)
            draft.delete()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


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


def load_first_template(request):
    """Loads the first template into the Designer."""
    print "load_first_template()"
    if request.method == 'POST':
        form = LoadTemplateForm(request.POST)
        if form.is_valid():
            # load the largest so wont overwrite objects when we load real one.
            draft_name = form.cleaned_data['draft_name']
            template_name = form.cleaned_data['template']
            draft_slug = slugify(draft_name)
            try:
                draft = smartgrid_mgr.get_designer_draft(draft_slug)
            except Http404:
                draft = Draft(name=draft_name, slug=draft_slug)
                draft.save()
            delete_me = Draft(name="delete-me-soon12341", slug='delete-me-soon12341')
            delete_me.save()
            smartgrid_mgr.load_example_grid(draft=delete_me, example_name='uh12')
            smartgrid_mgr.clear_designer(draft)
            if template_name != 'empty':
                smartgrid_mgr.clear_designer(draft=None)
                smartgrid_mgr.load_example_grid(draft, template_name)
            delete_me.delete()
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft.slug)
    return response


def load_template(request):
    """Loads a template into the given draft."""
    print "load_template()"
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
    user = request.user
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    settings, _ = GccSettings.objects.get_or_create(user=user)
    results = gcc.run_designer_checks(draft, settings)
    trees = action_dependency.build_designer_grid_trees(draft)
    unlock_tree = ''
    for k in list(trees):
        unlock_tree += trees[k].tohtmlstring()
        unlock_tree += '<p></p>'
    return HttpResponse(json.dumps({
            "errors": results[_ERRORS],
            "warnings": results[_WARNINGS],
            "dependency_trees": unlock_tree,
            }), mimetype="application/json")


def get_diff(request, draft_slug):
    """Returns the difference between the designer grid and the Smart Grid as a string."""
    _ = request
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    diff = smartgrid_mgr.diff_between_designer_and_grid(draft)
    return HttpResponse(json.dumps({
            "diff": diff,
            }), mimetype="application/json")


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
            if not predicate_mgr.validate_predicates(predicate):
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


def change_settings(request, draft_slug):
    """Changes the GccSettings for the user."""
    user = request.user
    settings, _ = GccSettings.objects.get_or_create(user=user)
    if request.method == "POST":
        form = GccSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
    response = HttpResponseRedirect("/sgg_designer/?draft=%s" % draft_slug)
    return response


def preview_library_action(request, action_slug):
    """Pre-views the LibraryAction with the given action_slug."""
    action = smartgrid_mgr.get_library_action(action_slug)
    view_objects = {}
    # if there is embedded widget, get the supplied objects
    if action.embedded_widget:
        view_module_name = 'apps.widgets.' + action.embedded_widget + '.views'
        view_objects[action.embedded_widget] = importlib.import_module(
            view_module_name).supply(request, None)
        view_objects['embedded_widget_template'] = "widgets/" + \
            action.embedded_widget + "/templates/index.html"

    return render_to_response("action.html", {
    "action": action,
    "view_objects": view_objects,
    }, context_instance=RequestContext(request))


def preview_draft_action(request, action_slug, draft_slug):
    """Pre-views the DesignerAction with the given action_slug and in the given draft."""
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    action = smartgrid_mgr.get_designer_action(draft=draft, slug=action_slug)
    view_objects = {}
    # if there is embedded widget, get the supplied objects
    if action.embedded_widget:
        view_module_name = 'apps.widgets.' + action.embedded_widget + '.views'
        view_objects[action.embedded_widget] = importlib.import_module(
            view_module_name).supply(request, None)
        view_objects['embedded_widget_template'] = "widgets/" + \
            action.embedded_widget + "/templates/index.html"

    return render_to_response("action.html", {
    "action": action,
    "view_objects": view_objects,
    }, context_instance=RequestContext(request))
