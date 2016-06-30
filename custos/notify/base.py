from .levels import INFO
from abc import ABCMeta, abstractmethod


class Notifier(metaclass=ABCMeta):
    def __init__(self, level=INFO, categories=('default', )):
        self.level = level
        self.categories = set(categories)

    def handle_message(self, msg):
        if self.categories.intersection(msg.categories) and msg.level > self.level:
            self.notify(msg)

    @abstractmethod
    def notify(self, msg):
        pass
