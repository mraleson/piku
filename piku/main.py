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

    # new command
    p = subparsers.add_parser('new', help='create new CircuitPython project')
    p.set_defaults(cmd=commands.new_command)

    # add command
    p = subparsers.add_parser('add', help='add library/module to project')
    p.set_defaults(cmd=commands.add_command)

    # remove command
    p = subparsers.add_parser('remove', help='remove library/module from project')
    p.set_defaults(cmd=commands.remove_command)

    # install command
    p = subparsers.add_parser('install', help='install project dependencies')
    p.set_defaults(cmd=commands.install_command)

    # serial command
    p = subparsers.add_parser('serial', help='connect usb serial port of device')
    p.set_defaults(cmd=commands.serial_command)

    # deploy command
    p = subparsers.add_parser('deploy', help='deploy project to device')
    p.set_defaults(cmd=commands.deploy_command)

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
