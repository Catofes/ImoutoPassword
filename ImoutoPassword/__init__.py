__author__ = 'herbertqiao'

from client import Client
import argparse
from daemon import basic_daemon


def start():
    parser = argparse.ArgumentParser(
    )
    subparsers = parser.add_subparsers(dest='operate')
    add_parser = subparsers.add_parser('add', alias=['a'],
                                       help='Generate a password')
    add_parser.add_argument('mark',
                            help="The mark of the password")
    add_parser.add_argument('-u', '--url',
                            help="The url of the password")
    add_parser.add_argument('-i', '--intro',
                            help="The intro of the password")
    add_parser.add_argument('-r', '--release',
                            help="The version of the password")
    del_parser = subparsers.add_parser('del', alias=['d'],
                                       help='Delete a password')
    ls_parser = subparsers.add_parser('ls', alias=['l'],
                                      help='List a password')
    get_parser = subparsers.add_parser('get', alias=['g'],
                                      help='List a password')
    daemon_parser = subparsers.add_parser('daemon', alias=['d'],
                                          help='Start the daemon')
    parser.add_argument('-c', '--config',
                        default='~/.ImoutoPassword/config',
                        help='Config file path')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='ImoutoPassword 0.0.1')
    args = parser.parse_args()
    print(args)
    Client(args)


if __name__ == '__main__':
    start()

