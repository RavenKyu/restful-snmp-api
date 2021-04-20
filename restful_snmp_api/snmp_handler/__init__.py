import datetime
import functools
import shlex

from restful_snmp_api.snmp_handler.handler import SnmpHandler
from restful_snmp_api.utils.logger import get_logger
from restful_snmp_api.snmp_handler.arugment_parser import \
    argument_parser

logger = get_logger('snmp-handler')


###############################################################################
class SnmpClient(SnmpHandler):
    def __init__(self, host, port,
                 community_read='public', community_write='private',
                 version=2):
        SnmpHandler.__init__(
            self, host, port, community_read, community_write, version)

    # =========================================================================
    def __enter__(self):
        return self

    # =========================================================================
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            import traceback
            traceback.print_exception(exc_type, exc_val, exc_tb)
        return

    # =========================================================================
    def response_handle(f):
        @functools.wraps(f)
        def func(*args, **kwargs):
            return f(*args, **kwargs)

        return func

    # =========================================================================
    def error_handle(f):
        @functools.wraps(f)
        def func(*args, **kwargs):
            return f(*args, **kwargs)

        return func

    # =========================================================================
    @error_handle
    @response_handle
    def snmp_get(self, command):
        parser = argument_parser()
        command = 'snmp_get ' + command
        spec = parser.parse_args(shlex.split(command))
        response = SnmpHandler.get(self, spec.oid)
        return response

    # =========================================================================
    @error_handle
    @response_handle
    def snmp_bulk(self, command):
        parser = argument_parser()
        command = 'snmp_bulk ' + command
        spec = parser.parse_args(shlex.split(command))
        response = SnmpHandler.bulk(self, spec.oid)
        return response

    # =========================================================================
    @error_handle
    @response_handle
    def snmp_table(self, command):
        parser = argument_parser()
        command = 'snmp_table ' + command
        spec = parser.parse_args(shlex.split(command))
        response = SnmpHandler.get_table(self, spec.oid)
        return response

    # =========================================================================
    @error_handle
    @response_handle
    def snmp_set(self, command):
        parser = argument_parser()
        command = 'snmp_set ' + command
        spec = parser.parse_args(shlex.split(command))
        dt = {'int': 'i', 'uint': 'u',
              'timeticks': 't',
              'ipaddress': 'a',
              'objid': 'o',
              'string': 's', 'hex': 'x',
              'decimal-string': 'd',
              'uint64b': 'U', 'int64b': 'I',
              'float': 'F', 'double': 'D'}[spec.data_type]
        response = SnmpHandler.set(self, spec.oid, spec.value, data_type=dt)
        return response


###############################################################################
class ExceptionResponse(Exception):
    pass


###############################################################################
def convert_type(value, data_type):
    raw = value
    dt = ('INT', 'UINT', 'UINT64B', 'INT64B', 'FLOAT', 'DOUBLE',
          'TIMETICKS', 'OBJID', 'STRING', 'DECIMAL-STRING', 'IPADDRESS')
    if data_type not in dt:
        raise TypeError(f"data type '{data_type}' is not supported.")

    if data_type in ('INT', 'UINT', 'UINT64B', 'INT64B'):
        value = int(value)
    elif data_type in ('FLOAT', 'DOUBLE'):
        value = float(value)
    elif 'IPADDRESS' == data_type:
        v = value.encode()
        raw = v.hex(' ')
        value = '.'.join(map(str, [int(x) for x in v]))
    elif data_type in ('TIMETICKS', 'OBJID', 'STRING', 'DECIMAL-STRING'):
        pass

    return raw, value


###############################################################################
def get_json_data_with_template(data: list, template):
    result = dict()
    result['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result['data'] = dict()

    for i, d in enumerate(data):
        raw = d['value']
        value = d['value']
        scale = None
        note = None
        try:
            t = next(x for x in template if x['key'] == d['key'])

            # converting type
            if 'type' in t and t['type']:
                try:
                    raw, value = convert_type(d['value'], t['type'])
                    if 'scale' in t and t['scale']:
                        value = value * t['scale']
                        scale = t['scale']
                except TypeError as e:
                    logger.warning(f"{d['key']}: {str(e)}")
                except ValueError as e:
                    logger.warning(
                        f"{d['key']}: failed to convert the value - "
                        f"data: {raw} -> {t['type']}")

            note = t['note']
        except StopIteration:
            pass

        if d['key'] in result['data']:
            logger.warning(f'There is already duplicated name, {d["key"]}')
        result['data'][d['key']] = {
            'raw': raw, 'value': value, 'scale': scale,
            'note': note
        }
    return result


###############################################################################
__all__ = ['get_json_data_with_template', ]
