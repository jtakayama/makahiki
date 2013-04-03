"""Provides the view of the widget."""
from apps.widgets.smartgrid.models import Level, Category, Filler
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from apps.widgets.smartgrid import smartgrid
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from apps.widgets.smartgrid_design.forms import SggUpdateForm, RevertToSmartgridForm, \
    DeployToSmartgridForm, ExampleGridsForm
from apps.widgets.smartgrid_library.models import LibraryActivity, LibraryEvent, \
    LibraryCommitment, LibraryCategory
from apps.managers.smartgrid_mgr import smartgrid_mgr, unlock_lint
import json
from apps.widgets.smartgrid_design.models import DesignerLevel, DesignerCategory, DesignerAction
from collections import OrderedDict


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    levels = DesignerLevel.objects.all()
    categories = LibraryCategory.objects.all()
    activities = LibraryActivity.objects.all()
    events = LibraryEvent.objects.all()
    commitments = LibraryCommitment.objects.all()
    fillers = Filler.objects.all()
    reset_form = RevertToSmartgridForm()
    publish_form = DeployToSmartgridForm()
    example_grid_form = ExampleGridsForm()
#    print len(activities)
#    print len(smartgrid_mgr.get_smartgrid_action_slugs())
#    print diff
    return {
        'levels': levels,
        'categories': categories,
        'activities': activities,
        'events': events,
        'commitments': commitments,
        'fillers': fillers,
        'reset_form': reset_form,
        'publish_form': publish_form,
        'example_grid_form': example_grid_form,
        'palette': smartgrid_mgr.get_designer_palette(),
        'smart_grid': smartgrid_mgr.get_designer_smartgrid(),
        'smart_grid_actions': smartgrid_mgr.get_designer_action_slugs(),
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


def update_sgg(request):
    """Handles the SggUpdateForm from the 'Save SGG' button."""
    if request.method == "POST":
        form = SggUpdateForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['category_updates']
            actions = form.cleaned_data['action_updates']

            num_levels = len(categories)
            if num_levels > 0:
                for lvl in xrange(0, num_levels):
                    level_cats = categories[lvl][1]
                    for i in xrange(0, len(level_cats), 4):
                        category = Category.objects.get(slug=level_cats[i])
                        category.priority = level_cats[i + 1]
                        category.name = level_cats[i + 2]
                        category.save()

                # clear the existing actions
#                for action in Action.objects.all():
#                    action.category = None
#                    action.level = None
#                    action.save()

#            num_levels = len(actions)
            for lvl in xrange(0, num_levels):
                level = Level.objects.get(name=actions[lvl][0])
                level_actions = actions[lvl][1]
                for i in xrange(0, len(level_actions), 6):
                    #slug = level_actions[i]
                    #type = level_actions[i + 1]
                    #cat_slug = level_actions[i + 2]
                    #priority = level_actions[i + 3] * 10
                    #text = level_actions[i + 4]
                    #pk = level_actions[i + 5]
                    category = Category.objects.get(slug=level_actions[i + 2])
                    if level_actions[i].startswith('filler'):
                        try:
                            action = Filler.objects.get(slug=level_actions[i])
                        except Filler.DoesNotExist:
                            action = Filler(name=level_actions[i + 4], slug=level_actions[i], \
                                            title=level_actions[i + 4], type='filler', \
                                            level=level, \
                                            category=category, priority=level_actions[i + 3] * 10)
                    else:
                        action = smartgrid.get_action(level_actions[i])
                    action.level = level
                    action.category = category
                    action.priority = level_actions[i + 3] * 10
                    action.save()

            response = HttpResponseRedirect("/sgg_designer/")
            return response

    raise Http404


def instantiate_category(request, cat_slug, level_slug, priority):
    """Instantiates the Smart Grid Game Category from the Library Category in the
    given level and with the given priority."""
    _ = request
    _ = level_slug
    lib_cat = LibraryCategory.objects.get(slug=cat_slug)
#    level = Level.objects.get(slug=level_slug)
    try:
        category = get_object_or_404(DesignerCategory, slug=cat_slug)
    except Http404:
        category = DesignerCategory()
    slug = lib_cat.slug
    category.name = lib_cat.name
    category.slug = slug
#    category.level = level  # there is no level....
    category.priority = priority
    category.save()

    #  Return the new pk for the instantiated category.
    return HttpResponse(json.dumps({
            "pk": category.pk,
            }), mimetype="application/json")


def instantiate_action(request, action_slug, cat_slug, level_slug, priority):
    """Instantiated the Smart Grid Game Action from the Library Action with the
    given level, category, and priority."""
    _ = request
    grid_action = smartgrid_mgr.instantiate_designer_from_library(action_slug)
    level = DesignerLevel.objects.get(slug=level_slug)
    grid_action.level = level
    grid_action.category = DesignerCategory.objects.get(slug=cat_slug)
    grid_action.priority = priority
    grid_action.save()

    #  Return the new pk for the instantiated action.
    return HttpResponse(json.dumps({
            "pk": grid_action.pk,
            }), mimetype="application/json")


def delete_action(request, action_slug):
    """Deletes the given Smart Grid Game Action."""
    _ = request
    action = smartgrid.get_action(action_slug)
    action.delete()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def delete_category(request, cat_slug):
    """Deletes the given Smart Grid Game Category."""
    _ = request
    category = get_object_or_404(Category, slug=cat_slug)
    category.delete()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def clear_from_grid(request, action_slug):
    """Clears the Level, Category, and priority for the given DesignerAction."""
    _ = request
    action = smartgrid_mgr.get_designer_action(action_slug)
    action.level = None
    action.category = None
    action.priority = 0
    action.save()
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
            smartgrid_mgr.deploy_designer_to_smartgrid()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def load_example_grid(request):
    """Clears the Designer and loads the example grid with the given name."""
    if request.method == 'POST':
        form = ExampleGridsForm(request.POST)
        if form.is_valid():
            example_name = form.cleaned_data['grid']
            smartgrid_mgr.load_example_grid(example_name)
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def run_lint(request):
    """Runs unlock_lint over the DesignerActions and shows the results in a page."""
    _ = request
    trees = unlock_lint.build_trees(DesignerAction)
    sorted_trees = OrderedDict(sorted(trees.items(), key=lambda t: -len(t[1])))
    unlock_tree = ''
    for k in list(sorted_trees):
        unlock_tree += sorted_trees[k].tohtmlstring()
        unlock_tree += '<p></p>'
    unreachable = unlock_lint.get_unreachable_actions(DesignerAction)
    false_unlock = unlock_lint.get_false_unlock_actions(DesignerAction)
    mismatched_levels = unlock_lint.get_missmatched_level(DesignerAction)
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
