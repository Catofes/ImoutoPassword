__author__ = 'herbertqiao'

from config import Config
from daemon.basic_daemon import BasicDaemon

class Client:
    def __init__(self, args):
        self.config = Config()