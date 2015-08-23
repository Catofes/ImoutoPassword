#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'herbertqiao'

from singleton import Singleton
import time
import json
from config import Config


def obj2dict(obj):
    d = {'__class__': obj.__class__.__name__, '__module__': obj.__module__}
    d.update(obj.__dict__)
    return d


def dict2obj(d):
    if "__class__" in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        args = dict((key, value) for key, value in d.item())
        inst = class_(**args)
    else:
        inst = d
    return inst


def to_json(obj):
    if isinstance(obj, Password):
        return {'__class__': 'Password',
                '__value__': obj2dict(obj)}
    raise TypeError(repr(obj) + ' is not JSON serializable')


def from_json(obj):
    if '__class__' in obj:
        if obj['__class__'] == "Password":
            return dict2obj(obj['__value__'])
    return obj


class Password():
    def __init__(self):
        self.id = 0
        self.user_id = 0
        self.mark = ""
        self.version = 0
        self.url = ""
        self.intro = ""
        self.type = 0
        self.update_time = time.time()
        self.need_update = False
        self.available = True
        self.visual = True
        self.sync_code = ""


class Storage(Singleton):
    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True
        self.version = 1
        self.database = {
            "version": 1,
            "passwords": [],
        }
        self.config = Config()
        self.storage_path = "~/.ImoutoPassword/database.json"

    def load(self):
        try:
            f = file(self.storage_path, 'r')
            self.database = json.loads(self.file.read(), object_hook=from_json)
            f.close()
        except:
            self.__init__()
        if not self.check_version():
            self.save()

    def save(self):
        f = file(self.storage_path, 'w')
        f.write(json.dumps(self.database, default=to_json))
        f.close()

    def check_version(self):
        if self.database["version"] == self.version:
            return True
        else:
            # Should do some update. Like    if self.database["version"] == 2 : self.database.["version"] = 3
            self.check_version()
            return False