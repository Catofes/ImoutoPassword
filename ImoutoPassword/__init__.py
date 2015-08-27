#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'herbertqiao'

from ImoutoPassword.client import Client
import argparse
from ImoutoPassword.daemon import basic_daemon
import time


def start():
    parser = argparse.ArgumentParser(
    )
    subparsers = parser.add_subparsers(dest='operate')
    add_parser = subparsers.add_parser('add', aliases=['a'],
                                       help='Generate a password')
    add_parser.add_argument('mark',
                            help="The mark of the password")
    add_parser.add_argument('-u', '--url',
                            help="The url of the password")
    add_parser.add_argument('-i', '--intro',
                            help="The intro of the password")
    add_parser.add_argument('-r', '--release',
                            help="The version of the password")
    add_parser.add_argument('-t', '--type',
                            choices=["def", "ncl", "wss", "abo", "no"],
                            default="def",
                            help="The type of the password. 'def'=>Default. 'ncl'=>No Capital Letter."
                                 " 'wss'=>With Special Symbol. 'abo'=>AlphaBet Only. 'no'=>Number Only.")
    add_parser.add_argument('-l', '--length',
                            help="The length of the password")
    add_parser.add_argument('-np', '--no-password', action="store_true",
                            help="Don't ask remember password and no password generate.")
    del_parser = subparsers.add_parser('del', aliases=['d'],
                                       help='Delete a password')
    del_parser.add_argument('id', type=int,
                            help="The id of the password")
    ls_parser = subparsers.add_parser('ls', aliases=['l'],
                                      help='List a password')
    ls_parser.add_argument('mark', default="", nargs='?',
                           help="The mark of the password")
    get_parser = subparsers.add_parser('get', aliases=['g'],
                                       help='List a password')
    get_parser.add_argument('mark', default="", nargs='?',
                            help="The mark of the password")
    daemon_parser = subparsers.add_parser('daemon',
                                          help='Start the daemon')
    parser.add_argument('--set-remember-password',
                        action='store_true',
                        help='Set the Remember Password')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='ImoutoPassword 0.0.1')
    args = parser.parse_args()
    client = Client()
    client.do(args)


if __name__ == '__main__':
    start()

