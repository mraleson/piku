#!/usr/bin/env python3
import sys
import argparse
import traceback
from piku import commands


def main():
    # create parser
    parser = argparse.ArgumentParser(description='')
    subparsers = parser.add_subparsers(dest='parser')
    parsers = {}

    # create command
    p = subparsers.add_parser('create', help='create new CircuitPython project')
    p.set_defaults(cmd=commands.create_command)
    p.add_argument('project', help='project name')

    # add command
    p = subparsers.add_parser('add', help='download and add module to project')
    p.set_defaults(cmd=commands.add_command)
    p.add_argument('module', help='module name [neopixel, file:/path/to/module.mpy]')

    # remove command
    p = subparsers.add_parser('remove', help='remove module from project')
    p.set_defaults(cmd=commands.remove_command)
    p.add_argument('module', help='module name [neopixel, my_module_name]')

    # install command
    p = subparsers.add_parser('install', help='install project dependencies')
    p.set_defaults(cmd=commands.install_command)

    # serial command
    p = subparsers.add_parser('serial', help='connect usb serial port of device')
    p.set_defaults(cmd=commands.serial_command)
    p.add_argument('-s', '--serial', default=None, help='serial port to connect to')

    # deploy command
    p = subparsers.add_parser('deploy', help='deploy project to device')
    p.set_defaults(cmd=commands.deploy_command)
    p.add_argument('-d', '--device', default=None, help='path of device to deploy to project to')
    p.add_argument('-y', '--yes', action='store_true', help='deploy to discovered device without confirmation dialog')

    # version command
    p = subparsers.add_parser('version', help='show piku version')
    p.set_defaults(cmd=commands.version_command)

    # info command
    p = subparsers.add_parser('info', help='show additional piku information')
    p.set_defaults(cmd=commands.info_command)
    p.add_argument('--clear-cache', action='store_true', help='clear module cache')
    p.add_argument('-m', '--modules', action='store_true', help='list availiable modules')

    # parse and execute
    args = parser.parse_args()
    if hasattr(args, 'cmd'):
        try:
            args.cmd(args)
        except Exception as exc:
            print(traceback.format_exc(), end='')
            print('Failed.')
        sys.exit()
    else:
        parsers.get(args.parser, parser).print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('')
