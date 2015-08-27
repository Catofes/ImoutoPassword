#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'herbertqiao'

from ImoutoPassword.storage import Storage, Password
from ImoutoPassword.config import Config
from ImoutoPassword.singleton import Singleton
from ImoutoPassword.password_type import PasswordType
from ImoutoPassword.errors import PasswordError
import re
from functools import cmp_to_key
import hashlib


class StaticDaemon(Singleton):
    def __init__(self):
        self.storage = Storage()
        self.config = Config()
        self.salt = self.config.get('option', 'salt')
        self.storage.load()
        self.database = self.storage.database
        self.password_type = PasswordType()

    def search(self, keyword=""):
        result = []
        if keyword == "":
            for pid, password in self.database['passwords'].items():
                if password.available and not password.special:
                    result.append(password)
            return result
        for pid, password in self.database['passwords'].items():
            if (re.search(keyword, password.mark) or re.search(keyword, password.intro)) \
                    and password.available and not password.special:
                result.append(password)
        return result

    def add(self, password):
        self.storage.lock.acquire()
        result = self.search(password.mark)
        version = 0
        for ele in result:
            if version < ele.version:
                version = ele.version
        version += 1
        password.version = version
        password.sync_code = "A"
        self.database['passwords_num'] += 1
        password.id = self.database['passwords_num']
        if password.length < 8 or password.length > 32:
            raise PasswordError("Password length illegal", "Password length should between 8 and 32.", password)
        self.database['passwords'][str(password.id)] = password
        self.storage.lock.release()
        self.storage.save()
        return password.id

    def remove(self, password_id):
        self.storage.lock.acquire()
        if str(password_id) in self.database['passwords'].keys():
            self.database['passwords'][str(password_id)].available = False
            self.database['passwords'][str(password_id)].sync_code = "M"
        self.storage.save()

    def get(self, remember_password, passwords_id):
        result = {}
        for pid in passwords_id:
            if str(pid) in self.database['passwords'].keys():
                password = self.database['passwords'][str(pid)]
                if password.special or not password.available:
                    continue
                key = self.calculate_key(remember_password, password)
                result[password] = key

        def compare(x, y):
            x=x[0]
            y=y[0]
            if x.mark > y.mark:
                return 1
            if x.mark < y.mark:
                return -1
            if x.version > y.version:
                return 1
            if x.version < y.version:
                return -1
            return 0

        return sorted(result.items(), key=cmp_to_key(compare))

    def modify(self, remember_password, password):
        self.storage.lock.acquire()
        password.sync_code = "M"
        if password.length < 4 or password.length > 32:
            raise PasswordError("Password length illegal", "Password length should between 4 and 32.", password)
        self.database['passwords'][str(password.id)].append(password)
        self.storage.lock.release()
        self.storage.save()

    def calculate_key(self, remember_password, password):
        result = remember_password + password.mark + str(password.version) + self.salt
        result = hashlib.sha512(result.encode('utf-8')).hexdigest()
        result = self.password_type.change(result, password.type, password.length)
        return result

    def check_remember_password(self, remember_password):
        check = None
        for id, password in self.database['passwords'].items():
            if password.special and password.mark == "RememberPasswordCheck":
                check = password
                break
        if not check:
            return -1
        if check.intro == self.calculate_key(remember_password, check):
            return 1
        else:
            return 0

    def generate_remember_password_check(self, remember_password):
        self.storage.lock.acquire()
        pid = 0
        password = Password()
        if self.check_remember_password(remember_password) != -1:
            for item in self.database['passwords']:
                if item.special and item.mark == "RememberPasswordCheck":
                    pid = item.id
                    password.sync_code = "M"
                    break
        else:
            self.database['passwords_num'] += 1
            pid = self.database['passwords_num']
            password.sync_code = "A"
        password.id = pid
        password.special = True
        password.mark = "RememberPasswordCheck"
        password.intro = self.calculate_key(remember_password, password)
        self.database['passwords'][str(pid)] = password
        self.storage.save()
        self.storage.lock.release()




