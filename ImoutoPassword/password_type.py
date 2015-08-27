__author__ = 'herbertqiao'

from ImoutoPassword.singleton import Singleton
from ImoutoPassword.errors import PasswordError


class PasswordType(Singleton):
    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True
        self.change_map = [
            {
                "name": "Default",
                "start_with": "Ip",
                "mapping": {
                    "a": "A",
                    "c": "C",
                    "e": "E"
                },
                "completion": ""
            },
            {
                "name": "No Capital Letter",
                "start_with": "",
                "mapping": {
                },
                "completion": ""
            },
            {
                "name": "With Special Symbol",
                "start_with": "Ip",
                "mapping": {
                    "a": "!",
                    "c": "."
                },
                "completion": ""
            },
            {
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
                "completion": ""
            },
            {
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
                "completion": "200253797761916324198679950268026"
            },

        ]
        pass

    def change(self, result, password_type, length):
        if password_type > len(self.change_map):
            raise PasswordError("Password type error.",
                                "Password type error. Check your password record or check your password_type file.",
                                None)
        change_map = self.change_map[password_type]
        for k, v in change_map['mapping'].items():
            result = result.replace(k, v)
        result = change_map["start_with"] + result + change_map['completion']
        result = result[0:length]
        return result
