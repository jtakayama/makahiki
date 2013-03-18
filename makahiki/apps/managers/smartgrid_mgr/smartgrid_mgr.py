'''Helper functions for the Smart Grid Game Library and grid instance.
Created on Mar 15, 2013

@author: Carleton Moore
'''

from django.db.models.deletion import Collector
from django.db.models.fields.related import ForeignKey
from apps.widgets.smartgrid.models import Action, Activity, Commitment, Event, Filler
from django.shortcuts import get_object_or_404
from apps.widgets.smartgrid_library.models import LibraryAction, LibraryActivity, LibraryCommitment,\
    LibraryEvent, LibraryCategory
from django.http import Http404


def duplicate(obj, value=None, field=None, duplicate_order=None):
    """
    Duplicate all related objects of obj setting
    field to value. If one of the duplicate
    objects has an FK to another duplicate object
    update that as well. Return the duplicate copy
    of obj.
    duplicate_order is a list of models which specify how
    the duplicate objects are saved. For complex objects
    this can matter. Check to save if objects are being
    saved correctly and if not just pass in related objects
    in the order that they should be saved.
    """
    collector = Collector({})
    collector.collect([obj])
    collector.sort()
    related_models = collector.data.keys()
    data_snapshot = {}
    for key in collector.data.keys():
        data_snapshot.update({key: dict(zip([item.pk for item in collector.data[key]], \
                                            [item for item in collector.data[key]]))})
    root_obj = None

    # Sometimes it's good enough just to save in reverse deletion order.
    if duplicate_order is None:
        duplicate_order = reversed(related_models)

    for model in duplicate_order:

        # Find all FKs on model that point to a related_model.
        fks = []
        for f in model._meta.fields:
            if isinstance(f, ForeignKey) and f.rel.to in related_models:
                fks.append(f)
        # Replace each `sub_obj` with a duplicate.
        if model not in collector.data:
            continue
        sub_objects = collector.data[model]
        for obj in sub_objects:
            for fk in fks:
                fk_value = getattr(obj, "%s_id" % fk.name)
                # If this FK has been duplicated then point to the duplicate.
                fk_rel_to = data_snapshot[fk.rel.to]
                if fk_value in fk_rel_to:
                    dupe_obj = fk_rel_to[fk_value]
                    setattr(obj, fk.name, dupe_obj)
            # Duplicate the object and save it.
            obj.id = None
            if field is None or field != 'slug':
                slug = obj.slug
                obj.slug = slug + '-copy'
            if field is not None:
                setattr(obj, field, value)
            obj.save()
            if root_obj is None:
                root_obj = obj
    return root_obj


def instantiate_grid_from_library(slug, value=None, field=None, duplicate_order=None):
    """Instantiates a Smart Grid Game instance from the Smart Grid Game Library instance.
    slug is the slug value for the library instance."""
    lib_obj = get_smartgrid_library_action(slug)
    action_type = lib_obj.type
    grid_obj = None
    if action_type == 'activity':
        grid_obj = Activity()
        lib_obj = LibraryActivity.objects.get(slug=slug)
    if action_type == 'commitment':
        grid_obj = Commitment()
        lib_obj = LibraryCommitment.objects.get(slug=slug)
    if action_type == 'event':
        grid_obj = Event()
        lib_obj = LibraryEvent.objects.get(slug=slug)
    if action_type == 'filler':
        grid_obj = Filler()

    for f in lib_obj._meta.fields:
        value = getattr(lib_obj, f.name)
        if f.name != 'id':
            print "%s, %s" % (f.name, value)
            setattr(grid_obj, f.name, value)

    # check to see if there is already a grid obj with the same slug
    try:
        obj = get_smartgrid_action(slug)
    except Http404:
        obj = None

    if obj is not None:
        slug = grid_obj.slug
        grid_obj.slug = slug + '-copy'
    grid_obj.save()

    return grid_obj


def get_smartgrid_action(slug):
    """returns the action object by slug."""
    return get_object_or_404(Action, slug=slug)


def get_smartgrid_library_action(slug):
    """Returns the Smart Grid Game Library Action for the given slug."""
    return get_object_or_404(LibraryAction, slug=slug)


def get_smartgrid_library_category(slug):
    """Return the Smart Grid Game Library Category for the given slug."""
    return get_object_or_404(LibraryCategory, slug=slug)
