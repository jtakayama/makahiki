'''Provides helpful methods for processing predicate logic statements.
Created on Jun 16, 2013

@author: Cam Moore
'''
import re


# Used to build the unlock_conditions
(_AND, _OR, _NOT, _TRUE, _FALSE) = (' and ', ' or ', 'not', 'True', 'False')


class Predicate(object):
    """Represents a predicate function with its parameters."""
    def __init__(self, name, parameter_list):
        """Constructor"""
        self.name = name
        self.parameter_list = parameter_list

    def __unicode__(self):
        """String representation of Predicate"""
        return "%s(%s)" % (self.name, self.parameter_list)

    def __str__(self):
        """String representation of Predicate"""
        return "%s(%s)" % (self.name, self.parameter_list)

    def __repr__(self):
        """String representation of Predicate"""
        return "<%s(%s)>" % (self.name, self.parameter_list)

    @classmethod
    def from_string(cls, s):
        """Creates a Predicate from a string."""
        parser = re.compile(r'([^(]+)\s*\(([^)]+)\)\s*')
        parsed = parser.findall(s)
        if len(parsed):
            name = parsed[0][0]
            parameter_list = parsed[0][1].split(', ')
            return cls(name, parameter_list)
        return None


def parse_clause(clause):
    """Returns """
    ret = []
    if '(' not in clause:
        return clause.split()
    if _NOT in clause:
        ret.append(_NOT)
        ret.append(Predicate.from_string(clause.split('not ')[1].strip()))
    else:
        ret.append(Predicate.from_string(clause.strip()))
    return ret


def parse_statement(statement):
    """Parses the statement into a list of operators and Predicates."""
    ret = []
    if '(' not in statement:
        return statement.split()
    else:
        if _AND in statement:
            for c in statement.split(_AND):
                ret.append(parse_clause(c))
                ret.append('and')
            ret.pop()
        elif _OR in statement:
            for c in statement.split(_OR):
                ret.append(parse_clause(c))
                ret.append('or')
            ret.pop()
        else:
            ret.append(parse_clause(statement))
    return ret
