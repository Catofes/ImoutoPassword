__author__ = 'herbertqiao'

class Error(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class PasswordError(Exception):
    def __init__(self, expression, message, password):
        self.expression = expression
        self.message = message
        self.password = password