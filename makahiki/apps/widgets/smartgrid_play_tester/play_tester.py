'''
Created on Jun 23, 2013

@author: Cam Moore
'''
from apps.widgets.smartgrid_design.models import DesignerLevel, DesignerColumnGrid, DesignerGrid, \
    DesignerAction
from apps.managers.predicate_mgr import predicate_mgr
from apps.widgets.notifications.models import UserNotification
from apps.widgets.smartgrid_play_tester.models import TesterActionSubmittion


def get_submitted_actions(user):
    """returns the completed action for the user. It is stored as a dict of action slugs and
    its member status."""
#     actions = cache_mgr.get_cache('smartgrid-completed-%s' % user.username)
    actions = {}
    for member in TesterActionSubmittion.objects.filter(user=user).\
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

    return predicate_mgr.eval_play_tester_predicates(predicates, user)


def availablity(action):
    """Returns -1 if the current date is before pub_date, 0 if action is available,
    and 1 if action is expired."""
    return 0


def get_designer_grid(draft, user):
    """Returns the play tester version of the Smart Grid Game for the given draft."""
    submitted_actions = get_submitted_actions(user)
    levels = []
    for level in DesignerLevel.objects.filter(draft=draft):
        level.is_unlock = predicate_mgr.eval_play_tester_predicates(level.unlock_condition, user)
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
                action = DesignerAction.objects.get(draft=draft, slug=row.action.slug)
                action.row = row.row
                if row.row > max_row:
                    max_row = row.row
                action.column = row.column
                if row.column > max_column:
                    max_column = row.column
                if action.slug in submitted_actions:
                    action.member = submitted_actions[action.slug]
                    action.is_unlock = True
                    action.completed = True
                else:
                    action.is_unlock = is_unlock(user, action)
                    action.completed = False

                action.availablity = availablity(action)
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
    