'''Dependency checking functionality for Library, Designer and Smartgrid Actions.
Created on May 16, 2013

@author: Cam Moore
'''
from apps.widgets.smartgrid_library.models import LibraryAction
from apps.widgets.smartgrid_design.models import DesignerAction, DesignerGrid
from apps.managers.smartgrid_mgr.gcc_model import ActionNode, DependencyTree, Error, Warn
from collections import OrderedDict


def __build_library_nodes():
    """Creates a list of ActionNodes for all the LibraryActions."""
    nodes = []
    for action in LibraryAction.objects.all():
        nodes.append(ActionNode(action, identifier=action.slug))
    return nodes


def __build_designer_nodes(draft):
    """Creates a list of ActionNodes for all the DesignerActions in the given Draft."""
    nodes = []
    for action in DesignerAction.objects.filter(draft=draft):
        locations = DesignerGrid.objects.filter(draft=draft, action=action)
        if len(locations) == 0:  # in palette
            nodes.append(ActionNode(action, identifier=action.slug))
        else:
            for loc in locations:
                nodes.append(ActionNode(action, level=loc.level, identifier=action.slug))
    return nodes


def __build_designer_grid_nodes(draft):
    """Creates a list of ActionNodes for the DesignerActions in the Designer grid for the given
    Draft."""
    nodes = []
    for action in DesignerAction.objects.filter(draft=draft):
        locations = DesignerGrid.objects.filter(draft=draft, action=action)
        for loc in locations:
            nodes.append(ActionNode(action, level=loc.level, identifier=action.slug))
    return nodes


def __get_submitted_action_slugs(node):
    """Returns the action slugs for submitted_action predicates in the given node's
    unlock_condition."""
    ret = []
    if node.unlock_condition:
        l = node.unlock_condition.split('submitted_action(')
        if len(l) > 1:
            index = l[1].find(')')
            ret.append(l[1][:index].strip('"\''))
            if len(l) > 2:
                index = l[1].find(')')
                ret.append(l[2][:index].strip('"\''))
    return ret


def __get_approved_action_slugs(node):
    """Returns the action slugs for approved_action predicates in the node's unlock_condition."""
    ret = []
    if node.unlock_condition:
        l = node.unlock_condition.split('approved_action(')
        if len(l) > 1:
            index = l[1].find(')')
            ret.append(l[1][:index].strip('"\''))
            if len(l) > 2:
                index = l[1].find(')')
                ret.append(l[2][:index].strip('"\''))
    return ret


def __get_dependent_action_slugs(node):
    """Returns the action slugs in the node's unlock_condition."""
    ret = []
    for slug in __get_submitted_action_slugs(node):
        ret.append(slug)
    for slug in __get_approved_action_slugs(node):
        ret.append(slug)
    return ret


def build_library_trees():
    """Builds the DependencyTrees for the LibraryActions."""
    nodes = __build_library_nodes()
    trees = {}
    for node in nodes:
        if node.unlock_condition == "True" or node.unlock_condition.find("or True") != -1 \
        or node.unlock_condition == "False" or node.unlock_condition.find("and False") != -1:
            t = DependencyTree()
            t.create_node(node.action, level=node.level, identifier=node.identifier)
            trees[node.identifier] = t
    for node in nodes:
        slugs = __get_dependent_action_slugs(node)
        for slug in slugs:
            for k in list(trees):
                if trees[k].get_node(slug):
                    trees[k].add_node(node, slug)
    for node in nodes:
        slugs = __get_dependent_action_slugs(node)
        for slug in slugs:
            for k in list(trees):
                if trees[k].get_node(slug):
                    trees[k].add_node(node, slug)
    return trees


def build_designer_grid_trees(draft):
    """Builds the DependencyTrees for the DesignerActions in the DesignerGrid."""
    nodes = __build_designer_grid_nodes(draft)
    trees = {}
    for node in nodes:
        if node.unlock_condition:
            if node.unlock_condition == "True" or node.unlock_condition.find("or True") != -1 \
            or node.unlock_condition == "False" or node.unlock_condition.find("and False") != -1:
                t = DependencyTree()
                t.create_node(node.action, level=node.level, identifier=node.identifier)
                trees[node.identifier] = t
    for i in range(10):
        _ = i
        for node in nodes:
            slugs = __get_dependent_action_slugs(node)
            for slug in slugs:
                for k in list(trees):
                    if trees[k].get_node(slug):
                        trees[k].add_node(node, slug)
    sorted_trees = OrderedDict(sorted(trees.items(), key=lambda t: -len(t[1])))
    return sorted_trees


def check_unreachable_designer_actions(draft):
    """Returns a list of Errors for each unreachable DesignerAction in the draft."""
    ret = []
    nodes = __build_designer_grid_nodes(draft)
    trees = build_designer_grid_trees(draft)
    # check all the nodes
    for node in nodes:
        in_tree = False
        for k in list(trees):
            tree = trees[k]
            if tree.get_node(node.identifier):
                in_tree = True
        if not in_tree:
            ret.append(Error(message="Action not reachable/unlockable [%s]" % \
                             node.action.unlock_condition, action=node.action))
    return ret


def check_false_unlock_designer_actions(draft):
    """Returns a list of Warnings for Designer actions whose root unlock_condition is False."""
    ret = []
    false_actions = []
    trees = build_designer_grid_trees(draft)
    for k in list(trees):
        tree = trees[k]
        root = tree.get_node(tree.root)
        if root:
            if root.unlock_condition == "False" or root.unlock_condition.find("and False") != -1:
                for node_key in list(tree.nodes):
                    node = tree.nodes[node_key]
                    if not node.action in false_actions and not node.action.type == 'filler':
                        false_actions.append(node.action)
    for action in false_actions:
        ret.append(Warn(message="Depends on action with False unlock condition", action=action))
    return ret


def check_missmatched_designer_level(draft):
    """Returns a list of Warnings for actions whose parent level is higher than their own."""
    ret = []
    trees = build_designer_grid_trees(draft)
    for k in list(trees):
        tree = trees[k]
        for node_key in list(tree.nodes):
            node = tree.nodes[node_key]
            if node.level:
                parent_name = node.parent
                if parent_name:
                    parent = tree.nodes[parent_name]
                    if parent and parent.level and parent.level.priority > node.level.priority:
                        message = "with %s Depends on action %s with higher level %s" % \
                            (node.level, parent.admin_link(), parent.level)
                        ret.append(Warn(message=message, action=node.action))
    return ret


def check_unreachable_library_actions():
    """Returns a list of Errors for each unreachable LibraryAction."""
    ret = []
    nodes = __build_library_nodes()
    trees = build_library_trees()
    # check all the nodes
    for node in nodes:
        in_tree = False
        for k in list(trees):
            tree = trees[k]
            if tree.get_node(node.identifier):
                in_tree = True
        if not in_tree:
            ret.append(Error(message="Action not reachable/unlockable", action=node.action))
    return ret


def check_false_unlock_library_actions():
    """Returns a list of Warnings for LibraryActions whose root unlock_condition is False."""
    ret = []
    false_actions = []
    trees = build_library_trees()
    for k in list(trees):
        tree = trees[k]
        root = tree.get_node(tree.root)
        if root:
            if root.unlock_condition == "False" or root.unlock_condition.find("and False"):
                for node_key in list(tree.nodes):
                    node = tree.nodes[node_key]
                    if not node.action in false_actions and not node.action.type == 'filler':
                        false_actions.append(node.action)
    for action in false_actions:
        ret.append(Warn(message="Depends on action with False unlock condition", action=action))
    return ret
