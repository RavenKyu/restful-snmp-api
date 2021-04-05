import argparse
import re
from restful_snmp_api.snmp_handler import *


###############################################################################
def regex_type_0or1(arg_value, pat=re.compile(r"^[0|1| ]*$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError('The values must be 0 or 1.')
    return arg_value


###############################################################################
class ActionMultipleTypeValues(argparse.Action):
    def __init__(
            self, option_strings, dest, const,
            nargs=None,
            default=None,
            type=None,
            required=False,
            help=None,
            metavar=None):
        super(ActionMultipleTypeValues, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            required=required,
            help=help,
            metavar=metavar)

    @staticmethod
    def _copy_items(items):
        if items is None:
            return []
        if type(items) is list:
            return items[:]
        import copy
        return copy.copy(items)

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = ActionMultipleTypeValues._copy_items(items)
        if 'add_bits' == self.const:
            values = list(map(int, values.replace(' ', '')))
            values.reverse()

        items.append((self.const, values))
        setattr(namespace, self.dest, items)


###############################################################################
def argument_parser():
    parent_parser = argparse.ArgumentParser(add_help=False)

    ###########################################################################
    essential_options_parser = argparse.ArgumentParser(add_help=False)
    essential_options_parser.add_argument(
        '-v', '--verbose', action='count')

    ###########################################################################
    parser = argparse.ArgumentParser(
        prog='',
        description='description',
        epilog='end of description', )

    sub_parser = parser.add_subparsers(dest='sub_parser')

    ###########################################################################
    snmp_get_parser = sub_parser.add_parser(
        'snmp_get', help='read snmp data',
        parents=[parent_parser, essential_options_parser],
        conflict_handler='resolve')
    snmp_get_parser.add_argument(
        '-o', '--oid', type=str, help='oid', action='append')

    ###########################################################################
    snmp_bulk_parser = sub_parser.add_parser(
        'snmp_bulk', help='read snmp bulk',
        parents=[parent_parser, essential_options_parser],
        conflict_handler='resolve')
    snmp_bulk_parser.add_argument('-o', '--oid', type=str, help='oid')

    ###########################################################################
    snmp_table_parser = sub_parser.add_parser(
        'snmp_table', help='read snmp table',
        parents=[parent_parser, essential_options_parser],
        conflict_handler='resolve')
    snmp_table_parser.add_argument(
        '-o', '--oid', type=str, help='oid', action='append')

    ###########################################################################
    snmp_set = sub_parser.add_parser(
        'snmp_set', help='set snmp data',
        parents=[parent_parser, essential_options_parser],
        conflict_handler='resolve')
    snmp_set.add_argument('oid', type=str, help='oid')
    snmp_set.add_argument('value', type=str, help='oid')
    snmp_set.add_argument('data_type', type=str,
                          choices=['int', 'uint', 'timeticks', 'ipaddress',
                                   'objid', 'string', 'hex', 'decimal-string',
                                   'uint64b', 'int64b', 'float', 'double'],
                          help='oid')

    return parser


__all__ = ['argument_parser', ]
