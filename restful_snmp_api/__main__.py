import argparse
import yaml
import pathlib
from restful_snmp_api.app import app
from restful_snmp_api.app import collector

MIB_DIRECTORY = pathlib.Path.home() / pathlib.Path('.snmp/mibs')


def argument_parser():
    parser = argparse.ArgumentParser('restful-modbus-api')
    parser.add_argument('-a', '--address', default='localhost',
                        help='host address')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='port')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-t', '--template_file', type=str, action='append')
    parser.add_argument('-m', '--mib_file', type=str, action='append')
    return parser


def main():
    parser = argument_parser()
    argspec = parser.parse_args()

    if argspec.template_file:
        for t in argspec.template_file:
            with open(t, 'r') as f:
                schedules = yaml.safe_load(f)
            collector.add_job_schedules(schedules)

    if argspec.mib_file:
        for t in argspec.mib_file:
            source = pathlib.Path(t)
            if not source.exists():
                raise FileNotFoundError(f'{t} is not existed.')
            target = (MIB_DIRECTORY / source.name)
            if target.exists():
                logging.warning(
                    f'{source.name} is already existed in {MIB_DIRECTORY}.')
            target.write_text(source.read_text())  # for text files
            logging.info(f'{source.name} is copied to {MIB_DIRECTORY}.')

    app.run(host=argspec.address,
            port=argspec.port,
            debug=argspec.debug)


if __name__ == '__main__':
    main()
