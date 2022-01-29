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

    # deploy command
    p = subparsers.add_parser('deploy', help='deploy project to device')
    p.set_defaults(cmd=commands.deploy)

    # serial command
    p = subparsers.add_parser('serial', help='connect usb serial port of device')
    p.set_defaults(cmd=commands.serial)
    p.add_argument('-d', '--dns', type=str, default="1.1.1.1", help='specify dns server [default 1.1.1.1]')

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
