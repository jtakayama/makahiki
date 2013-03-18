"""Provides the view of the widget."""
from apps.widgets.smartgrid.models import Level, Category, Activity, Event, Commitment, \
    Filler
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from apps.widgets.smartgrid import smartgrid
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from apps.widgets.sgg_design.forms import SggUpdateForm
from apps.widgets.smartgrid_library.models import LibraryActivity, LibraryEvent, LibraryCommitment,\
    LibraryCategory, LibraryAction
from apps.managers.smartgrid_mgr import smartgrid_mgr


def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    levels = Level.objects.all()
    categories = Category.objects.all()
    activities = LibraryActivity.objects.all()
    events = LibraryEvent.objects.all()
    commitments = LibraryCommitment.objects.all()
    form = SggUpdateForm({'category_updates': '[]',
                          'action_updates': '[]'})

#    print len(activities)
#    print len(smartgrid.get_smart_grid_action_slugs())
    return {
        'levels': levels,
        'categories': categories,
        'activities': activities,
        'events': events,
        'commitments': commitments,
        'form': form,
        'smart_grid': smartgrid.get_smart_grid(),
        'smart_grid_actions': smartgrid.get_smart_grid_action_slugs()
            }


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
    lib_cat = LibraryCategory.objects.get(slug=cat_slug)
    level = Level.objects.get(slug=level_slug)
    category = Category()
    slug = lib_cat.slug
    slug += '-'
    slug += level.slug
    slug += '-'
    slug += priority
    category.name = lib_cat.name
    category.slug = slug
    category.level = level  # there is no level....
    category.priority = priority
    category.save()
    print category.pk
    response = HttpResponseRedirect("/sgg_designer/")
    return response


def instantiate_action(request, action_slug, cat_slug, level_slug, priority):
    """Instantiated the Smart Grid Game Action from the Library Action with the
    given level, category, and priority."""
    _ = request
    grid_action = smartgrid_mgr.instantiate_grid_from_library(action_slug)
    level = Level.objects.get(slug=level_slug)
    grid_action.level = level
    grid_action.category = Category.objects.get(slug=cat_slug)
    grid_action.priority = priority
    grid_action.save()
    response = HttpResponseRedirect("/sgg_designer/")
    return response


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
