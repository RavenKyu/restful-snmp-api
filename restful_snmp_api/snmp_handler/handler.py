from easysnmp import Session
from functools import wraps
from easysnmp import snmp_get, snmp_set, snmp_walk
from restful_snmp_api.utils.logger import get_logger


################################################################################
class SnmpHandler:
    # ==========================================================================
    def __init__(self, host, port, community_read='public',
                 community_write='private', version=2):
        self.host = host
        self.port = port
        self.logger = get_logger('snmp-handler')
        self.address = (host, port)
        self.community_read = community_read
        self.community_write = community_write
        self.version = version

    # ==========================================================================
    def result(self):
        @wraps(self)
        def func(*args, **kwargs):
            this = args[0]
            try:
                result = self(*args, **kwargs)
                ok, value, message = (True, result, '')
            except Exception as e:
                this.logger.exception(msg=str(e), exc_info=e)
                ok, value, message = (False, None, str(e))
            if not ok:
                this.logger.error(f'code: {ok} message: {message}')
            return ok, value, message

        return func

    # ==========================================================================
    @result
    def get(self, items: list):
        result = list()
        for oid in items:
            r = snmp_get(oid, hostname=self.host,
                         community=self.community_read, version=self.version)
            result.append((oid, r.value))
        return result

    # ==========================================================================
    @result
    def bulk(self, oid):
        r = snmp_walk(oid, hostname=self.host,
                      community=self.community_read, version=self.version)
        values = [(f'{oid}.{v.oid_index}', v.value) for v in r]
        return values

    # ==========================================================================
    @result
    def get_table(self, objs):
        """
        :param objs:
             external_sensor_configuration_table = [
            'PDU2-MIB::externalSensorSerialNumber',
            'PDU2-MIB::externalSensorName',
            'PDU2-MIB::externalSensorDescription',]
        :return:
            code: True data:
            {'1': {'externalSensorSerialNumber': '1EQ9100045',
               'externalSensorName': 'Temperature 1',
               'externalSensorChannelNumber': '1',
               'externalSensorUnits': 'degreeC',
               'externalSensorDecimalDigits': '1',
               'externalSensorMaximum': '800', 'externalSensorMinimum': '-350',
               'externalSensorIsActuator': 'false',
               'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:1'},
            '2': {'externalSensorSerialNumber': '1EQ9100045',
               'externalSensorName': 'Relative Humidity 1',
               'externalSensorChannelNumber': '1',
               'externalSensorUnits': 'percent',
               'externalSensorDecimalDigits': '0',
               'externalSensorMaximum': '100', 'externalSensorMinimum': '0',
               'externalSensorIsActuator': 'false',
               'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:1'},
            '4': {'externalSensorSerialNumber': '1EQ9703299',
               'externalSensorName': 'Temperature 2',
               'externalSensorChannelNumber': '1',
               'externalSensorUnits': 'degreeC',
               'externalSensorDecimalDigits': '1',
               'externalSensorMaximum': '800', 'externalSensorMinimum': '-350',
               'externalSensorIsActuator': 'false',
               'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:2'},
            '5': {'externalSensorSerialNumber': '1EQ9703299',
               'externalSensorName': 'Relative Humidity 2',
               'externalSensorChannelNumber': '1',
               'externalSensorUnits': 'percent',
               'externalSensorDecimalDigits': '0',
               'externalSensorMaximum': '100', 'externalSensorMinimum': '0',
               'externalSensorIsActuator': 'false',
               'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:2'},
            '6': {'externalSensorSerialNumber': '1EQ9703299',
               'externalSensorName': 'Absolute Humidity 2',
               'externalSensorChannelNumber': '1',
               'externalSensorUnits': 'grampercubicmeter',
               'externalSensorDecimalDigits': '1',
               'externalSensorMaximum': '3000', 'externalSensorMinimum': '0',
               'externalSensorIsActuator': 'false',
               'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:2'},
            '7': {'externalSensorSerialNumber': '1GE4900096',
               'externalSensorName': 'Door Handle Lock 1',
               'externalSensorChannelNumber': '1',
               'externalSensorUnits': 'none',
               'externalSensorDecimalDigits': '0',
               'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
               'externalSensorIsActuator': 'true',
               'externalSensorPosition': 'ONBOARD'},
            '8': {'externalSensorSerialNumber': '1GE4900096',
               'externalSensorName': 'Door Handle Lock 2',
               'externalSensorChannelNumber': '2',
               'externalSensorUnits': 'none',
               'externalSensorDecimalDigits': '0',
               'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
               'externalSensorIsActuator': 'true',
               'externalSensorPosition': 'ONBOARD'},
            '9': {'externalSensorSerialNumber': '1GE4900096',
               'externalSensorName': 'Door 1',
               'externalSensorChannelNumber': '1',
               'externalSensorUnits': 'none',
               'externalSensorDecimalDigits': '0',
               'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
               'externalSensorIsActuator': 'false',
               'externalSensorPosition': 'ONBOARD'},
            '10': {'externalSensorSerialNumber': '1GE4900096',
                'externalSensorName': 'Door Lock 1',
                'externalSensorChannelNumber': '1',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'ONBOARD'},
            '11': {'externalSensorSerialNumber': '1GE4900096',
                'externalSensorName': 'Door 2',
                'externalSensorChannelNumber': '2',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'ONBOARD'},
            '12': {'externalSensorSerialNumber': '1GE4900096',
                'externalSensorName': 'Door Lock 2',
                'externalSensorChannelNumber': '2',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'ONBOARD'},
            '13': {'externalSensorSerialNumber': 'QLL0300014',
                'externalSensorName': 'Dry Contact 1',
                'externalSensorChannelNumber': '1',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'true',
                'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:3'},
            '14': {'externalSensorSerialNumber': 'QLL0300014',
                'externalSensorName': 'Dry Contact 2',
                'externalSensorChannelNumber': '2',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'true',
                'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:3'},
            '15': {'externalSensorSerialNumber': 'QLL0300014',
                'externalSensorName': 'Hall Effect 1',
                'externalSensorChannelNumber': '-1',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:3'},
            '16': {'externalSensorSerialNumber': 'QLL0300014',
                'externalSensorName': 'On/Off 1',
                'externalSensorChannelNumber': '1',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:3'},
            '17': {'externalSensorSerialNumber': 'QLL0300014',
                'externalSensorName': 'On/Off 2',
                'externalSensorChannelNumber': '2',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:3'},
            '18': {'externalSensorSerialNumber': 'QLL0300014',
                'externalSensorName': 'On/Off 3',
                'externalSensorChannelNumber': '3',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:3'},
            '19': {'externalSensorSerialNumber': 'QLL0300014',
                'externalSensorName': 'On/Off 4',
                'externalSensorChannelNumber': '4',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:3'},
            '20': {'externalSensorSerialNumber': 'QLL0300014',
                'externalSensorName': 'On/Off 5',
                'externalSensorChannelNumber': '5',
                'externalSensorUnits': 'none',
                'externalSensorDecimalDigits': '0',
                'externalSensorMaximum': '0', 'externalSensorMinimum': '0',
                'externalSensorIsActuator': 'false',
                'externalSensorPosition': 'DEVICE-1WIREPORT:1;CHAIN-POSITION:3'}}
        """

        result = dict()
        for d in objs:
            ok, value, msg = self.bulk(d)

            if not ok:
                raise ValueError(msg)
            for v in value:
                name = v[0]
                _, index, number = v[0].split('.')
                if number not in result:
                    result[number] = dict()
                result[number][name] = v[1]

        r = list()
        for k in result.keys():
            result[k]['id'] = k
            r.append(result[k])
        return r

    # ==========================================================================
    @result
    def set(self, oid: str, value, data_type='i'):
        """
        :param oid: 'PDU2-MIB::externalSensorType.1.1'
        :param value: 8
        :param data_type:
        :return:
        """
        s = Session(hostname=self.host,
                    community=self.community_write,
                    version=self.version)
        r = s.set(oid, value, data_type)
        return r
