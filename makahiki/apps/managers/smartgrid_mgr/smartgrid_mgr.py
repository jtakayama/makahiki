'''Helper functions for the Smart Grid Game Library and grid instance.
Created on Mar 15, 2013

@author: Carleton Moore
'''

from django.db.models.deletion import Collector
from django.db.models.fields.related import ForeignKey
from apps.widgets.smartgrid.models import Action, Activity, Commitment, Event, Filler, Category, \
    Level, TextPromptQuestion
from django.shortcuts import get_object_or_404
from apps.widgets.smartgrid_library.models import LibraryAction, LibraryActivity, \
    LibraryCommitment, LibraryEvent, LibraryCategory
from django.http import Http404
from apps.widgets.smartgrid_design.models import DesignerAction, DesignerCategory, \
    DesignerActivity, DesignerCommitment, DesignerEvent, DesignerFiller, DesignerLevel,\
    DesignerTextPromptQuestion


def duplicate(obj, value=None, field=None, duplicate_order=None):  # pylint: disable=R0914
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
# pylint: enable=R0914


def is_library(obj):
    """Returns True if the object is a Library instance."""
    cls = type(obj).__name__
    return cls.startswith('Library')


def is_designer(obj):
    """Returns True if the object is a Designer instance."""
    cls = type(obj).__name__
    return cls.startswith('Designer')


def is_smartgrid(obj):
    """Returns True if the object is a SmartGrid instance."""
    return not (is_library(obj) or is_designer(obj))


def _copy_fields(orig, copy):
    """Copies the field values from orig to copy and saves the copy."""
    for f in orig._meta.fields:
        if f.name != 'id':
            value = getattr(orig, f.name)
            setattr(copy, f.name, value)
    copy.save()


def _copy_fields_no_foriegn_keys(orig, copy):
    """Copies the field values from orig to copy and saves the copy."""
    fks = []
    for f in orig._meta.fields:
        if isinstance(f, ForeignKey):
            fks.append(f.name)
#    print fks
    for f in orig._meta.fields:
        if f.name != 'id' and not f.name in fks:
            value = getattr(orig, f.name)
            setattr(copy, f.name, value)


def _copy_action_fields(orig, copy):  # pylint: disable=R0912
    """Copies the field values from orig to copy and saves the copy."""
    # Find all FKs on model that point to a related_model.
    fks = []
    copy_fields = []
    for f in copy._meta.fields:
        copy_fields.append(f.name)
        if isinstance(f, ForeignKey):
            fks.append(f.name)
    for f in orig._meta.fields:
        if f.name in copy_fields:
            if f.name != 'id':
                if f.name not in fks:
                    value = getattr(orig, f.name)
                    setattr(copy, f.name, value)
                else:
                    value = getattr(orig, f.name)
                    if value:
                        slug = value.slug
                    if f.name == 'level' and value:
                        if is_designer(copy):
                            value = DesignerLevel.objects.get(slug=slug)
                        if is_smartgrid(copy):
                            value = Level.objects.get(slug=slug)
                    if f.name == 'category' and value:
                        if is_designer(copy):
                            value = DesignerCategory.objects.get(slug=slug)
                        if is_smartgrid(copy):
                            value = Category.objects.get(slug=slug)
                    setattr(copy, f.name, value)
    copy.save()  # pylint: enable=R0912


def instantiate_designer_from_library(slug):
    """Instantiates a Smart Grid Game Design instance from the Smart Grid Game Library instance.
    slug is the slug value for the library instance. If the Design instance exists it is over
    written."""
    lib_obj = get_library_action(slug)
    action_type = lib_obj.type
    exist_obj = None
    try:
        exist_obj = get_designer_action(slug)
    except Http404:
        exist_obj = None
    design_obj = None
    if exist_obj == None:
        if action_type == 'activity':
            design_obj = DesignerActivity()
            lib_obj = LibraryActivity.objects.get(slug=slug)
        if action_type == 'commitment':
            design_obj = DesignerCommitment()
            lib_obj = LibraryCommitment.objects.get(slug=slug)
        if action_type == 'event':
            design_obj = DesignerEvent()
            lib_obj = LibraryEvent.objects.get(slug=slug)
        if action_type == 'filler':
            design_obj = DesignerFiller()
    else:  # use the existing instance.
        design_obj = exist_obj

    _copy_action_fields(lib_obj, design_obj)

    return design_obj


def instantiate_designer_from_grid(slug):
    """Creates a designer instance from the Smart Grid instance."""
    grid_obj = get_smartgrid_action(slug)
    action_type = grid_obj.type
    old_obj = None
    try:
        old_obj = get_designer_action(slug)
    except Http404:
        old_obj = None
    designer_obj = None
    if old_obj == None:
        if action_type == 'activity':
            designer_obj = DesignerActivity()
            grid_obj = Activity.objects.get(slug=slug)
        if action_type == 'commitment':
            designer_obj = DesignerCommitment()
            grid_obj = Commitment.objects.get(slug=slug)
        if action_type == 'event':
            designer_obj = DesignerEvent()
            grid_obj = Event.objects.get(slug=slug)
        if action_type == 'filler':
            designer_obj = DesignerFiller()
            grid_obj = Filler.objects.get(slug=slug)
    else:
        designer_obj = old_obj
    _copy_action_fields(grid_obj, designer_obj)

    return designer_obj


def instantiate_grid_from_designer(slug):
    """Creates a Smart Grid instance from the designer instance."""
    designer_obj = get_designer_action(slug)
    action_type = designer_obj.type
    old_obj = None
    try:
        old_obj = get_smartgrid_action(slug)
    except Http404:
        old_obj = None
    grid_obj = None
    if old_obj == None:
        if action_type == 'activity':
            grid_obj = Activity()
            designer_obj = DesignerActivity.objects.get(slug=slug)
        if action_type == 'commitment':
            grid_obj = Commitment()
            designer_obj = DesignerCommitment.objects.get(slug=slug)
        if action_type == 'event':
            designer_obj = DesignerEvent.objects.get(slug=slug)
            grid_obj = Event()
        if action_type == 'filler':
            designer_obj = DesignerFiller.objects.get(slug=slug)
            grid_obj = Filler()
    else:
        grid_obj = old_obj
    _copy_action_fields(designer_obj, grid_obj)

    return grid_obj


def get_designer_action(slug):
    """Returns the Smart Grid Game Designer Action for the given slug."""
    action = get_object_or_404(DesignerAction, slug=slug)
    pk = action.pk
    if action.type == 'activity':
        return DesignerActivity.objects.get(pk=pk)
    if action.type == 'commitment':
        return DesignerCommitment.objects.get(pk=pk)
    if action.type == 'event':
        return DesignerEvent.objects.get(pk=pk)
    if action.type == 'filler':
        return DesignerFiller.objects.get(pk=pk)
    return action


def get_designer_action_slugs():
    """Returns the DesignerAction slugs that are currently in the Smart Grid Designer.
    This includes the actions in the palette that don't have levels or categories."""
    action_list = []
    for action in DesignerAction.objects.all():
        action_list.append(action.slug)
    return action_list


def get_designer_category(slug):
    """Return the Smart Grid Game Library Category for the given slug."""
    return get_object_or_404(DesignerCategory, slug=slug)


def get_library_action(slug):
    """Returns the Smart Grid Game Library Action for the given slug."""
    action = get_object_or_404(LibraryAction, slug=slug)
    pk = action.pk
    if action.type == 'activity':
        return LibraryActivity.objects.get(pk=pk)
    if action.type == 'commitment':
        return LibraryCommitment.objects.get(pk=pk)
    if action.type == 'event':
        return LibraryEvent.objects.get(pk=pk)
    return action


def get_library_category(slug):
    """Return the Smart Grid Game Library Category for the given slug."""
    return get_object_or_404(LibraryCategory, slug=slug)


def get_smartgrid_action(slug):
    """returns the action object by slug."""
    action = get_object_or_404(Action, slug=slug)
    pk = action.pk
    if action.type == 'activity':
        return Activity.objects.get(pk=pk)
    if action.type == 'commitment':
        return Commitment.objects.get(pk=pk)
    if action.type == 'event':
        return Event.objects.get(pk=pk)
    if action.type == 'filler':
        return Filler.objects.get(pk=pk)
    return action


def get_smartgrid_action_slugs():
    """Returns the Actions that are currently in the Smart Grid."""
    action_list = []
    for level in Level.objects.all():
        for action in level.action_set.all().select_related('category'):
            action_list.append(action.slug)
    return action_list


def get_smartgrid_category(slug):
    """returns the category object by slug."""
    return get_object_or_404(Category, slug=slug)


def get_smartgrid():
    """Returns the currently defined smart grid."""
    levels = []
    for level in Level.objects.all():
        categories = []
        action_list = None
        category = None
        for action in level.action_set.all().select_related("category"):
            # the action are ordered by level and category
            if category != action.category:
                if category:
                    # a new category
                    category.task_list = action_list
                    categories.append(category)

                action_list = []
                category = action.category

            action_list.append(action)

        if category:
            # last category
            category.task_list = action_list
            categories.append(category)

        level.cat_list = categories
        levels.append(level)

    return levels


def get_designer_smartgrid():
    """Returns the currently defined smart grid."""
    levels = []
    for level in DesignerLevel.objects.all():
        categories = []
        action_list = None
        category = None
        for action in level.designeraction_set.all().select_related("category"):
            # the action are ordered by level and category
            if category != action.category:
                if category:
                    # a new category
                    category.task_list = action_list
                    categories.append(category)

                action_list = []
                category = action.category

            action_list.append(action)

        if category:
            # last category
            category.task_list = action_list
            categories.append(category)

        level.cat_list = categories
        levels.append(level)

    return levels


def get_designer_palette():
    """Returns the DesignerActions with no Level or no Category.  These actions will not
    appear in the grid if published."""
    palette = []
    for action in DesignerAction.objects.all():
        if action.level == None or action.category == None:
            palette.append(action)
    return palette


def clear_designer():
    """Deletes all the instances in the designer."""
    for obj in DesignerLevel.objects.all():
        obj.delete()
    for obj in DesignerCategory.objects.all():
        obj.delete()
    for obj in DesignerAction.objects.all():
        obj.delete()


def copy_smartgrid_to_designer():
    """Copies the current Smart Grid Game to the designer instances."""
    # Clear out the Designer
    clear_designer()
    # Copy the levels
    for lvl in Level.objects.all():
        des_lvl = DesignerLevel()
        _copy_fields(lvl, des_lvl)
    # Copy the categories
    for cat in Category.objects.all():
        des_cat = DesignerCategory()
        _copy_fields(cat, des_cat)
    # Copy the Actions
    for action in Action.objects.all():
        instantiate_designer_from_grid(action.slug)
    # Copy all the TextPropmtQuestions
    for question in TextPromptQuestion.objects.all():
        slug = question.action.slug
        des_obj = DesignerTextPromptQuestion()
        _copy_fields_no_foriegn_keys(question, des_obj)
        des_obj.action = get_designer_action(slug)
        des_obj.save()


def clear_smartgrid():
    """Unsets all the Actions' Level and Category."""
    for action in Action.objects.all():
        action.level = None
        action.category = None
        action.save()


def deploy_designer_to_smartgrid():
    """Clears the current Smart Grid Game and copies the designer instances to the
    Smart Grid Game. Clearing the grid does not delete the actions just clears their
    Levels and Categories."""
    clear_smartgrid()
    for action in DesignerAction.objects.all():
        instantiate_grid_from_designer(action.slug)


def is_diff_between_designer_and_grid_action(slug):
    """Returns True if there is a difference between the Designer Action and
    Grid Action with the given slug."""
    grid = get_smartgrid_action(slug)
    fks = []
    for f in grid._meta.fields:
        if isinstance(f, ForeignKey):
            fks.append(f.name)
    designer = get_designer_action(slug)
    for f in grid._meta.fields:
        if f.name in fks:
            if not f.name.endswith('_ptr'):
                grid_val = getattr(grid, f.name).name
                designer_val = getattr(designer, f.name).name
                if grid_val != designer_val:
                    return True
        elif f.name != 'id':
            grid_val = getattr(grid, f.name)
            designer_val = getattr(designer, f.name)
            if grid_val != designer_val:
                return True
    return False


def diff_between_designer_and_grid_action(slug):
    """Returns a list of the fields that are different between the Designer Action and
    Grid Action with the given slug."""
    grid = get_smartgrid_action(slug)
    fks = []
    for f in grid._meta.fields:
        if isinstance(f, ForeignKey):
            fks.append(f.name)
    designer = get_designer_action(slug)
    diff = []
    for f in grid._meta.fields:
        if f.name in fks:
            if not f.name.endswith('_ptr'):
                grid_val = getattr(grid, f.name).name
                designer_val = getattr(designer, f.name).name
                if grid_val != designer_val:
                    diff.append(f.name)
        elif f.name != 'id':
            grid_val = getattr(grid, f.name)
            designer_val = getattr(designer, f.name)
            if grid_val != designer_val:
                diff.append(f.name)
    return diff
