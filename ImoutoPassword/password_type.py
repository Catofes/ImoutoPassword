__author__ = 'herbertqiao'

from ImoutoPassword.singleton import Singleton
from ImoutoPassword.errors import PasswordError
import re


class PasswordType(Singleton):
    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True
        self.change_map = {
            "def": {
                "name": "Default",
                "start_with": "",
                "mapping": {
                    "a": "A",
                    "c": "C",
                    "e": "E"
                },
                "regexp": [
                    {
                        "reg": "[A-Z]",
                        "add_at_head": "I",
                        "add_at_end": ""
                    },
                    {
                        "reg": "[a-z]",
                        "add_at_head": "i",
                        "add_at_end": ""
                    },
                    {
                        "reg": "[0-9]",
                        "add_at_head": "",
                        "add_at_end": "1",
                    },
                ],
                "completion": ""
            },
            "ncl": {
                "name": "No Capital Letter",
                "start_with": "",
                "mapping": {
                },
                "regexp": [
                    {
                        "reg": "[a-z]",
                        "add_at_head": "i",
                        "add_at_end": ""
                    },
                    {
                        "reg": "[0-9]",
                        "add_at_head": "",
                        "add_at_end": "1",
                    },
                ],
                "completion": ""
            },
            "wss": {
                "name": "With Special Symbol",
                "start_with": "",
                "mapping": {
                    "a": "!",
                    "c": "."
                },
                "regexp": [
                    {
                        "reg": "[A-Z]",
                        "add_at_head": "I",
                        "add_at_end": ""
                    },
                    {
                        "reg": "[a-z]",
                        "add_at_head": "i",
                        "add_at_end": ""
                    },
                    {
                        "reg": "[0-9]",
                        "add_at_head": "",
                        "add_at_end": "1",
                    },
                    {
                        "reg": "[.!]",
                        "add_at_head": "",
                        "add_at_end": ".",
                    },
                ],
                "completion": ""
            },
            "abo": {
                "name": "AlphaBet Only",
                "start_with": "",
                "mapping": {
                    "0": "h",
                    "1": "i",
                    "2": "j",
                    "3": "k",
                    "4": "l",
                    "5": "m",
                    "6": "n",
                    "7": "o",
                    "8": "p",
                    "9": "q",
                },
                "regexp": [],
                "completion": ""
            },
            "no": {
                "name": "Number Only",
                "start_with": "",
                "mapping": {
                    "a": "",
                    "b": "",
                    "c": "",
                    "d": "",
                    "e": "",
                    "f": "",
                },
                "regexp": [],
                "completion": "200253797761916324198679950268026"
            },
        }
        pass

    def change(self, result, password_type, length):
        if password_type not in self.change_map.keys():
            raise PasswordError("Password type error.",
                                "Password type error. Check your password record or check your password_type file.",
                                None)
        change_map = self.change_map[password_type]
        for k, v in change_map['mapping'].items():
            result = result.replace(k, v)
        for item in change_map['regexp']:
            result = result[0:length]
            if not re.search(item['reg'], result):
                result = (item['add_at_head'] + result)[0:length]
                result = result[0:length - len(item['add_at_end'])] + item['add_at_end']
        result = change_map["start_with"] + result + change_map['completion']
        result = result[0:length]
        return result
