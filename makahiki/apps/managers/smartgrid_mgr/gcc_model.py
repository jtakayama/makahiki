'''Defines the common object used by the Grid Consistency Checker.
Created on May 19, 2013

@author: Carm Moore
'''
from collections import deque
from django.template.defaultfilters import slugify


class Error(object):
    """Represents Errors detected by GCC."""
    def __init__(self, action, message):
        """Initializer."""
        self.action = action
        self.message = message

    def __unicode__(self):
        return "Error: %s on %s" % (self.message, self.action)

    def __str__(self):
        return "Error: %s on %s" % (self.message, self.action)

    def __repr__(self):
        return "<Error: %s[%s]>" % (self.action, self.message)

    def get_admin_link(self):
        """Returns the action's admin link."""
        return self.action.admin_link()


class Warn(object):
    """Represents Warnings detected by GCC."""
    def __init__(self, action, message):
        """Initializer."""
        self.action = action
        self.message = message

    def __unicode__(self):
        return "Warning: %s on %s" % (self.message, self.action)

    def __str__(self):
        return "Warning: %s on %s" % (self.message, self.action)

    def __repr__(self):
        return "<Warning: %s[%s]>" % (self.action, self.message)

    def get_admin_link(self):
        """Returns the action's admin link."""
        return self.action.admin_link()
(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)


class ActionNode(object):
    """Node in unlock condition tree. Identifier is the slug of the action, parent
    is the slug of the unlock condition dependence."""

    def __init__(self, action, level=None, identifier=None, expanded=True):
        """Initializer"""
        self.__identifier = action.slug if identifier is None else slugify(identifier)
        self.action = action
        self.level = level
        self.expanded = expanded
        self.__parent = None
        self.__children = []

    def __unicode__(self):
        return "%s[%s]" % (self.action, self.action.unlock_condition)

    def __str__(self):
        return "%s[%s]" % (self.action, self.action.unlock_condition)

    def __repr__(self):
        return "<ActionNode: %s[%s]>" % (self.action, self.action.unlock_condition)

    def admin_link(self):
        """Returns the admin link for the action."""
        return self.action.admin_link()

    @property
    def identifier(self):
        """The Identifier property."""
        return self.__identifier

    @property
    def parent(self):
        """The Parent property."""
        return self.__parent

    @parent.setter
    def parent(self, value):
        """Sets the Parent property."""
        if value is not None:
            self.__parent = slugify(value)

    @property
    def children(self):
        """The Children property."""
        return self.__children

    @children.setter
    def children(self, value):
        """Sets the Children property."""
        if value is not None and isinstance(value, list):
            self.__children = value

    @property
    def name(self):
        """The Name property."""
        return self.action

    @property
    def unlock_condition(self):
        """The unlock_condition property."""
        return self.action.unlock_condition

    def update_children(self, identifier, mode=_ADD):
        """Updates the children with the given identifier and mode."""
        slug = slugify(identifier)
        if mode is _ADD:
            if slug not in self.__children:
                self.__children.append(slug)
            elif mode is _DELETE:
                if slug in self.__children:
                    self.__children.remove(slug)
            elif mode is _INSERT:
                self.__children = [slug]


class MultipleRootError(Exception):
    """Multiple Root problem in Tree."""
    pass


class DependencyTree(object):
    """Unlock Condition dependency tree for Library, Designer, or Smartgrid Actions."""
    def __init__(self):
        """Initializer"""
        self.nodes = {}
        self.root = None

    def add_node(self, node, parent=None):
        """Adds a ActionNode to the DependencyTree."""
        if parent is None:
            if self.root is not None:
                raise MultipleRootError
            else:
                self.root = node.identifier
        try:
            self.nodes[node.identifier]
        except KeyError:
            self.nodes.update({node.identifier: node})
        self.__update_children(parent, node.identifier, _ADD)

    def create_node(self, action, level=None, identifier=None, parent=None):
        """Create a child ActionNode for the ActionNode indicated by the 'parent' parameter."""
        node = ActionNode(action, level=level, identifier=identifier)
        self.add_node(node, parent)
        return node

    def expand_tree(self, nid=None, mode=_DEPTH, filter_fn=None):
        """expands the tree."""
        # Python generator. Loosly based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        def real_true(pos):
            """always return True."""
            _ = pos
            return True

        if nid is None:
            nid = self.root
        if filter_fn is None:
            filter_fn = real_true

        if filter_fn(nid):
            yield nid
            queue = self[nid].children
            while queue:
                if filter_fn(queue[0]):
                    yield queue[0]
                    expansion = self[queue[0]].children
                    if mode is _DEPTH:
                        queue = expansion + queue[1:]  # depth-first
                    elif mode is _WIDTH:
                        queue = queue[1:] + expansion  # width-first
                else:
                    queue = queue[1:]

    def get_node(self, nid):
        """Returns the node with the given nid, or None if node is not in the tree."""
        try:
            return self.nodes[nid]
        except KeyError:
            return None

    def is_branch(self, nid):
        """Return the following nodes of [nid]"""
        return self[nid].children

    def move_node(self, source, destination):
        """Move a node indicated by the 'source' parameter to the parent node
        indicated by the 'dest' parameter"""
        parent = self[source].parent
        self.__update_children(parent, source, _DELETE)
        self.__update_children(destination, source, _ADD)
        self.__update_parent(source, destination)

    def paste(self, nid, new_tree):
        """Paste a new tree to the original one by linking the root
of new tree to nid."""
        assert isinstance(new_tree, DependencyTree)

        # check identifier replication

        if set(new_tree.nodes) & set(self.nodes):
            # error, duplicate node identifier
            raise ValueError('Duplicated nodes exists.')

        new_tree[new_tree.root].parent = nid
        self.__update_children(nid, new_tree.root, _ADD)
        self.nodes.update(new_tree.nodes)

    def remove_node(self, identifier):
        """Remove a node indicated by 'identifier'. All the successors are removed, too."""
        parent = self[identifier].parent
        remove = []  # temp. list for nodes which will be removed
        for pid in self.expand_tree(identifier):
            # check if node has children
            # true -> run remove_node with child_id
            # no -> delete node
            remove.append(pid)

        for pid in remove:
            del(self.nodes[pid])

        self.__update_children(parent, identifier, _DELETE)

    def rsearch(self, nid, filter_fn=None):
        """Search the tree from nid to the root along links reversedly."""

        def real_true(p):
            """always return True."""
            _ = p
            return True

        if filter_fn is None:
            filter_fn = real_true
        current = nid
        while current is not None:
            if filter_fn(current):
                yield current
            current = self[current].parent

    def show(self, nid=None, level=_ROOT):
        """"Another implementation of printing tree using Stack
Print tree structure in hierarchy style.
For example:
Root
|___ C01
| |___ C11
| |___ C111
| |___ C112
|___ C02
|___ C03
| |___ C31
A more elegant way to achieve this function using Stack structure,
for constructing the Nodes Stack push and pop nodes with additional level info."""
        leading = ''
        lasting = '|___ '

        if nid is None:
            nid = self.root
        label = "{0}:{1}[{2}]".format(self[nid].level, self[nid].action, self[nid].action.unlock_condition)

        queue = self[nid].children
        #print level
        if level == _ROOT:
            print(label)
        else:
            if level <= 1:
                leading += ('|' + ' ' * 4) * (level - 1)
            else:
                leading += ('|' + ' ' * 4) + (' ' * 5 * (level - 2))
            print("{0}{1}{2}".format(leading, lasting, label))

        if self[nid].expanded:
            level += 1
            for element in queue:
                self.show(element, level)  # recursive call

    def tohtmlstring(self, nid=None):
        """builds string like show w/o recursion."""
        s = ''
        lvl = _ROOT
        nodes_to_visit = deque([])
        if nid is None:
            nid = self.root
        nodes_to_visit.append((self[nid], lvl))
        while len(nodes_to_visit) > 0:
            leading = ''
            lasting = '|___ '
            current_node, lvl = nodes_to_visit.popleft()
            for c in current_node.children:
#                print "child {0} lvl{1}".format(self[c], lvl + 1)
                nodes_to_visit.appendleft((self[c], lvl + 1))
#            print "process = {0} lvl{1}".format(current_node, lvl)

            label = "{0}: <b>{1}</b>[{2}]".format(current_node.level, \
                                                  current_node.action.admin_link(), \
                                                  current_node.action.unlock_condition)
            if lvl == _ROOT:
                s += label + '<br/>'
            else:
                if lvl <= 1:
                    leading += ('|' + '&nbsp' * 4) * (lvl - 1)
                else:
                    leading += ('|' + '&nbsp' * 4) + ('&nbsp' * 5 * (lvl - 2))
                s += "{0}{1}{2}".format(leading, lasting, label) + '<br/>'
        return s

    def subtree(self, nid):
        """Return a COPY of subtree of the whole tree with the nid being the new root.
And the structure of the subtree is maintained from the old tree."""
        st = DependencyTree()
        st.root = nid
        for node_n in self.expand_tree(nid):
            st.nodes.update({self[node_n].identifier: self[node_n]})
        return st

    def __contains__(self, identifier):
        """Returns something."""
        return [node.identifier for node in self.nodes
                if node.identifier is identifier]

    def __getitem__(self, key):
        """Returns something."""
        return self.nodes.get(key)

    def __len__(self):
        """Returns something."""
        return len(self.nodes)

    def __setitem__(self, key, item):
        """Returns something."""
        self.nodes.update({key: item})

    def __update_parent(self, nid, identifier):
        """Returns something."""
        self[nid].parent = identifier

    def __update_children(self, nid, identifier, mode):
        """Returns something."""
        if nid is None:
            return False
        else:
            if self[nid]:
                self[nid].update_children(identifier, mode)
                return True
            return False

    def __repr__(self):
        return "<DependencyTree: %s>" % (self.root)
