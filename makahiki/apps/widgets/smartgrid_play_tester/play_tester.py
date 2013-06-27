'''
Created on Jun 23, 2013

@author: Cam Moore
'''
from apps.widgets.smartgrid_design.models import DesignerLevel, DesignerColumnGrid, DesignerGrid
from apps.managers.predicate_mgr import predicate_mgr
from apps.widgets.notifications.models import UserNotification
from apps.widgets.smartgrid_play_tester.models import TesterActionSubmittion
from apps.managers.smartgrid_mgr import smartgrid_mgr


def annotate_action_details(user, action):
    """Retrieve the action details for the given user evaluated in the testing environment"""
    if action.type == "commitment":
        submittions = TesterActionSubmittion.objects.filter(user=user, action=action).\
            order_by("-submission_date")
        # calculate the task duration
        action.duration = action.commitment_length
    else:
        submittions = TesterActionSubmittion.objects.filter(user=user, action=action)
        # calculate the task duration
        if action.type == "activity":
            duration = action.expected_duration
        else:  # is event
            if action.type in ("event", "excursion"):
                duration = action.expected_duration
            else:
                duration = 0

        hours = duration / 60
        minutes = duration % 60
        action.duration = ""
        if hours > 1:
            action.duration = "%d hours" % hours
        elif hours > 0:
            action.duration = "%d hour" % hours
        if minutes > 0:
            action.duration += " %d minutes" % minutes

    if submittions:
        action.member = submittions[0]
        action.is_unlock = True
        action.completed = True
    else:
        action.member = None
        action.is_unlock = is_unlock(user, action)
        for loc in DesignerGrid.objects.filter(action=action):
            action.is_unlock = action.is_unlock and is_level_unlock(user, loc.level, action.draft)
        action.completed = False
    action.availablity = availablity(action)
    return action


def can_add_commitment(user):
    """Returns true for all users."""
    _ = user
    return True


def is_level_unlock(user, level, draft):
    """return True if the level is unlock."""
    return level and predicate_mgr.eval_play_tester_predicates(level.unlock_condition, user, draft)


def get_submitted_actions(user, draft_slug):
    """returns the completed action for the user. It is stored as a dict of action slugs and
    its member status."""
#     actions = cache_mgr.get_cache('smartgrid-completed-%s' % user.username)
    draft = smartgrid_mgr.get_designer_draft(draft_slug)
    actions = {}
    for member in TesterActionSubmittion.objects.filter(draft=draft, user=user).\
        select_related("action").order_by("-submission_date"):
        slug = member.action.slug
        if  member.action.type != "commitment":
            actions[slug] = {"approval_status": member.approval_status,
                             }
        elif slug not in actions:
            actions[slug] = {"days_left": member.days_left(),
                             "award_date": member.award_date,
                             }
#         cache_mgr.set_cache('smartgrid-completed-%s' % user, actions, 1800)
    return actions


def is_unlock(user, action):
    """Returns the unlock status of the user action."""
    return eval_unlock(user, action)


def eval_unlock(user, action):
    """Determine the unlock status of a task by dependency expression"""
    predicates = action.unlock_condition
    if not predicates:
        return False
    draft = smartgrid_mgr.get_designer_draft(action.draft)
    return predicate_mgr.eval_play_tester_predicates(predicates, user, draft)


def availablity(action):
    """Returns -1 if the current date is before pub_date, 0 if action is available,
    and 1 if action is expired."""
    _ = action
    return 0


def get_designer_grid(draft, user):  # pylint: disable=R0914,R0912
    """Returns the play tester version of the Smart Grid Game for the given draft."""
    levels = []
    for level in DesignerLevel.objects.filter(draft=draft):
        level.is_unlock = predicate_mgr.eval_play_tester_predicates(level.unlock_condition,
                                                                    user=user, draft=draft)
        if level.is_unlock:  # only include unlocked levels
            if level.unlock_condition != "True":
                contents = "%s is unlocked." % level
                obj, created = UserNotification.objects.\
                    get_or_create(recipient=user,
                                  contents=contents,
                                  level=UserNotification.LEVEL_CHOICES[2][0])
                if created:  # only show the notification if it is new
                    obj.display_alert = True
                    obj.save()
            level_ret = []
            level.is_complete = True
            level_ret.append(level)
            level_ret.append(DesignerColumnGrid.objects.filter(draft=draft, level=level))
#                level_ret.append(Grid.objects.filter(level=level))

            max_column = len(DesignerColumnGrid.objects.filter(draft=draft, level=level))
            max_row = 0
            just_actions = []
            # update each action
            for row in DesignerGrid.objects.filter(draft=draft, level=level):
                action = smartgrid_mgr.get_designer_action(draft=draft, slug=row.action.slug)
                action.row = row.row
                if row.row > max_row:
                    max_row = row.row
                action.column = row.column
                if row.column > max_column:
                    max_column = row.column
                action = annotate_action_details(user, action)
                # if there is one action is not completed, set the level to in-completed
                if not action.completed:
                    level.is_complete = False
                just_actions.append(action)
            level_ret.append(just_actions)
            columns = []
            for cat in level_ret[1]:
                if cat.column not in columns:
                    columns.append(cat.column)
            for act in level_ret[2]:
                if act.column not in columns:
                    columns.append(act.column)
            level_ret.append(columns)
            level_ret.append(max_column)
            level_ret.append(max_row)
            levels.append(level_ret)
        else:
            level_ret = []
            level_ret.append(level)
            level_ret.append([])
            level_ret.append([])
            level_ret.append([])
            level_ret.append(0)
            level_ret.append(0)
            levels.append(level_ret)
    return levels
# pylint: enable=R0914,R0912


def can_complete_commitment(user, commitment):
    """Returns true."""
    _ = user
    _ = commitment
    return False
