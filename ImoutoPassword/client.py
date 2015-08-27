#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'herbertqiao'

from ImoutoPassword.config import Config
from ImoutoPassword.daemon.static_daemon import StaticDaemon
from ImoutoPassword.storage import Password
import re
import getpass
import time


class Client:
    def __init__(self):
        self.config = Config()
        self.daemon = StaticDaemon()

    def color_print(self, input_color, mes):
        if input_color == 'r':
            fore = 31
        elif input_color == 'g':
            fore = 32
        elif input_color == 'b':
            fore = 36
        elif input_color == 'y':
            fore = 33
        else:
            fore = 37
        input_color = "\x1B[%d;%dm" % (1, fore)
        return "%s%s\x1B[0m" % (input_color, mes)

    def color_keyword(self, value, keyword=""):
        split = re.split(keyword, value)
        result = ""
        for i in range(0, len(split) - 1):
            result += split[i]
            result += self.color_print('r', keyword)
        result += split[len(split) - 1]
        return result

    def add_space(self, value, length=0):
        value += " " * length
        return value

    def to_text(self, table, origin_table):
        line_number = len(origin_table)
        if line_number <= 1:
            return
        column_number = len(origin_table[0])
        column_width = [0 for i in range(0, column_number)]
        for line in origin_table:
            for i in range(0, column_number):
                if column_width[i] < len(str(line[i])):
                    column_width[i] = len(str(line[i]))
        for i in range(0, line_number):
            for j in range(0, column_number):
                print(self.add_space(str(table[i][j]), column_width[j] - len(str(origin_table[i][j]))) + "\t", end="")
            print("\n", end="")

    def print_password(self, passwords, keyword="", show_key=True):
        table = []
        origin_table = []
        if show_key:
            table.append(["Id", "Mark", "Password", "Version", "Intro", "URL"])
            origin_table.append(["Id", "Mark", "Password", "Version", "Intro", "URL"])
            for password in passwords:
                table.append(
                    [password[0].id, self.color_keyword(password[0].mark, keyword), password[1], password[0].version,
                     self.color_keyword(password[0].intro, keyword), self.color_keyword(password[0].url, keyword)])
                origin_table.append(
                    [password[0].id, password[0].mark, password[1], password[0].version, password[0].intro,
                     password[0].url])
        else:
            table.append(["Id", "Mark", "Version", "Intro", "URL"])
            origin_table.append(["Id", "Mark", "Version", "Intro", "URL"])
            for password in passwords:
                table.append([password[0].id, self.color_keyword(password[0].mark, keyword), password[0].version,
                              self.color_keyword(password[0].intro, keyword),
                              self.color_keyword(password[0].url, keyword)])
                origin_table.append(
                    [password[0].id, password[0].mark, password[0].version, password[0].intro, password[0].url])
        self.to_text(table, origin_table)

    def do(self, args):
        if args.operate == "add" or args.operate == "a":
            password = Password()
            password.mark = str(args.mark)
            if args.url:
                password.url = str(args.url)
            if args.intro:
                password.intro = str(args.intro)
            if args.release:
                password.version = int(args.release)
            if args.length:
                password.length = int(args.length)
            if args.type:
                if args.type == "def":
                    password.type = 0
                elif args.type == "ncl":
                    password.type = 1
                elif args.type == "wss":
                    password.type = 2
                elif args.type == "abo":
                    password.type = 3
                elif args.type == "no":
                    password.type = 4
                else:
                    password.type = 0
            if args.no_password or self.config.get("option", "add_without_rpw") == "1":
                self.daemon.add(password)
                return
            remember_password = getpass.getpass("Please input your remember password:")
            if self.config.get("option", "rpw_check") == "1":
                if self.daemon.check_remember_password(remember_password) != 1:
                    print("Remember Password Error. Please check or set your remember password.")
                    return
            pw_id = self.daemon.add(password)
            result = self.daemon.get(remember_password, [pw_id])
            self.print_password(result)
            return
        if args.operate == "del" or args.operate == "d":
            self.daemon.remove(args.id)
            return
        if args.operate == "ls" or args.operate == "l":
            if not args.mark:
                keyword = ""
            else:
                keyword = args.mark
            passwords = self.daemon.search(keyword)
            passwords = self.daemon.get("", [value.id for value in passwords])
            self.print_password(passwords, keyword, False)
            return
        if args.operate == "get" or args.operate == "g":
            remember_password = getpass.getpass("Please input your remember password:")
            if self.config.get("option", "rpw_check") == "1":
                if self.daemon.check_remember_password(remember_password) != 1:
                    print("Remember Password Error. Please check or set your remember password.")
                    return
            if not args.mark:
                keyword = ""
            else:
                keyword = args.mark
            passwords = self.daemon.search(keyword)
            passwords = self.daemon.get(remember_password, [value.id for value in passwords])
            self.print_password(passwords, keyword, True)
            return
        if not args.operate:
            if args.set_remember_password:
                remember_password = getpass.getpass("Please input your remember password:")
                retype_remember_password = getpass.getpass("Please retype your remember password:")
                if remember_password != retype_remember_password:
                    print("Password didn't match. Please try again.")
                    return
                self.daemon.generate_remember_password_check(remember_password)
            return