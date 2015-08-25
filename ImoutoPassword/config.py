#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'herbertqiao'

import ConfigParser
import string
import os
import io
import sys
from singleton import Singleton


class Config(Singleton):
    def __init__(self, args=None):
        if hasattr(self, '_init'):
            return
        self._init = True
        self.args = args
        self.config = ConfigParser.ConfigParser(
        )
        if args:
            self.config_path = args.config
        else:
            self.config_path = "~/.ImoutoPassword/config"
        self.config_default_file = """
        [option]
        #Whether to check the main password right or not.
        check_password = true
        #Salt.
        salt = ha92

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
        self.config_default = ConfigParser.ConfigParser()
        self.config_default.readfp(io.BytesIO(self.config_default_file))
        self.load()

    def create_config_file(self):
        config_file = file(self.config_path, "w")
        config_file.write(self.config_default_file)
        config_file.close()

    def load(self):
        if not os.path.isfile(self.config_path):
            self.create_config_file()
        try:
            self.config.read(self.config_path)
        except Exception:
            print("Read Config File Error.")
            sys.exit(1)

    def save(self):
        config_file = file(self.config_path, "w")
        config_file.write(self.config)
        config_file.close()

    def get(self, section, option):
        try:
            result = self.config.get(section, option)
        except Exception:
            result = self.config_default.get(section, option)
        return result



