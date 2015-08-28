#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'herbertqiao'

import configparser
import string
import os
import io
import sys
from ImoutoPassword.singleton import Singleton


class Config(Singleton):
    def __init__(self, args=None):
        if hasattr(self, '_init'):
            return
        self._init = True
        self.args = args
        self.config = configparser.ConfigParser(
        )

        self.config_path = os.path.join(os.path.expanduser('~'), '.ImoutoPassword')
        self.config_file = os.path.join(os.path.expanduser('~'), '.ImoutoPassword/config')
        self.config_default_file = """
[option]
#Whether to check the main password right or not.
check_password = true
#Salt.
salt = ImoutoPassword
#Check master password is right or not.
mpw_check = 1
#When add new password, don't ask for master_password
add_without_mpw = 0

[daemon]
#Whether to enable daemon mode.
daemon = 1
#Main password stored time in second.
expired = 300
#listen port
port = 8912

[sync]
#sync enable
enable = 0
#server url
server = https://test.com/api
        """
        self.config_default = configparser.ConfigParser()
        self.config_default.read_string(self.config_default_file)
        self.load()

    def create_config_file(self):
        if not os.path.isdir(self.config_path):
            os.mkdir(self.config_path)
        config_file = open(self.config_file, "w")
        config_file.write(self.config_default_file)
        config_file.close()

    def load(self):
        if not os.path.isfile(self.config_file):
            self.create_config_file()
        try:
            self.config.read(self.config_file)
        except Exception:
            print("Read Config File Error.")
            sys.exit(1)

    def save(self):
        config_file = open(self.config_file, "w")
        config_file.write(self.config)
        config_file.close()

    def get(self, section, option):
        try:
            result = self.config.get(section, option)
        except Exception:
            result = self.config_default.get(section, option)
        return result



