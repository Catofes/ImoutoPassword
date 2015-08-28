#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'herbertqiao'

from ImoutoPassword.singleton import Singleton
import time
import json
import threading
from ImoutoPassword.config import Config
import os


def obj2dict(obj):
    d = {'__class__': obj.__class__.__name__, '__module__': obj.__module__}
    d.update(obj.__dict__)
    return d


def dict2obj(d):
    if "__class__" in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        modules = module_name.split('.')
        module = __import__(module_name)
        for i in range(1, len(modules)):
            module = getattr(module, modules[i])
        class_ = getattr(module, class_name)
        args = dict((key, value) for key, value in d.items())
        inst = class_(**args)
    else:
        inst = d
    return inst


def to_json(obj):
    if isinstance(obj, Password):
        return {'__json_class__': 'Password',
                '__json_value__': obj2dict(obj)}
    raise TypeError(repr(obj) + ' is not JSON serializable')


def from_json(obj):
    if '__json_class__' in obj:
        if obj['__json_class__'] == "Password":
            return dict2obj(obj['__json_value__'])
    return obj


class Password():
    def __init__(self, id=0, user_id=0, mark="", version=0, length=16, url="", intro="", structure_version=1,
                 type="def", update_time=0, encrypt=False, need_update=False, available=True, special=False,
                 sync_code=""):
        self.id = id
        self.user_id = user_id
        self.mark = mark
        self.version = version
        self.length = length
        self.url = url
        self.intro = intro
        self.type = type
        self.structure_version = structure_version
        self.encrypt = encrypt
        self.update_time = time.time()
        if update_time != 0:
            self.update_time = update_time
        self.need_update = need_update
        self.available = available
        self.special = special
        self.sync_code = sync_code


class Storage(Singleton):
    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True
        self.version = 1
        self.database = {
            "version": 1,
            "passwords": {},
            "passwords_num": 0
        }
        self.config = Config()
        self.storage_path = os.path.join(os.path.expanduser('~'), '.ImoutoPassword/database.json')
        self.lock = threading.RLock()

    def load(self):
        try:
            f = open(self.storage_path, 'r')
            self.database = json.loads(f.read(), object_hook=from_json)
            f.close()
        except:
            self.__init__()
        if not self.check_version():
            self.save()

    def save(self):
        f = open(self.storage_path, 'w')
        f.write(json.dumps(self.database, default=to_json))
        f.close()

    def check_version(self):
        if self.database["version"] == self.version:
            return True
        else:
            # Should do some update. Like    if self.database["version"] == 2 : self.database.["version"] = 3
            self.check_version()
            return False