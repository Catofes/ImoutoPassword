__author__ = 'herbertqiao'

from ImoutoPassword.storage import Storage, Password
from ImoutoPassword.config import Config
from ImoutoPassword.singleton import Singleton
from ImoutoPassword.password_type import PasswordType
from ImoutoPassword.errors import PasswordError
import re
import hashlib


class StaticDaemon(Singleton):
    def __init__(self):
        self.storage = Storage()
        self.config = Config()
        self.salt = self.config.get('option', 'salt')
        self.storage.load()
        self.database = self.storage.database
        self.password_type = PasswordType()

    def search(self, keyword):
        result = []
        for password in self.database['passwords']:
            if (re.match(keyword, password.mark) or re.match(keyword, password.intro)) \
                    and password.available and password.visual:
                result.append(password)
        return result

    def add(self, remember_password, password):
        self.storage.lock.acquire()
        password.sync_code = "A"
        self.database['passwords_num'] += 1
        password.id = self.database['passwords_num']
        if password.length < 4 or password.length > 32:
            raise PasswordError("Password length illegal", "Password length should between 4 and 32.", password)
        password.check = self.calculate_check_code(self.calculate_key(remember_password, password))
        self.database['passwords'][str(password.id)].append(password)
        self.storage.lock.release()
        self.storage.save()

    def remove(self, password_id):
        self.storage.lock.acquire()
        if str(password_id) in self.storage['passwords'].keys():
            self.database['passwords'][str(password_id)].available = False
        self.storage.save()

    def get(self, remember_password, passwords_id):
        result = {}
        for pid in passwords_id:
            if str(pid) in self.storage['passwords'].keys():
                password = self.storage['passwords'][str(pid)]
                key = self.calculate_key(remember_password, password)
                result[password] = key
                if self.calculate_check_code(key) != password.check_code:
                    raise PasswordError("Password check error.", "Please check your remember password and salt.",
                                        password)
        return result

    def modify(self):
        pass

    def calculate_key(self, remember_password, password):
        result = remember_password + password.mark + str(password.version) + self.salt
        result = hashlib.sha512(result).hexdigest()
        result = self.password_type.change(result, password.type, password.length)
        return result

    @staticmethod
    def calculate_check_code(value):
        return hashlib.sha512(value)[0:16]




