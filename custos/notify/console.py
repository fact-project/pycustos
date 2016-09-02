import logging

from .base import Notifier

log = logging.getLogger(__name__)


class ConsoleNotifier(Notifier):
    '''
    A simple notifier class to output notifications to the console.
    '''
    def notify(self, recipient, msg):
        print(
            'Message: {}    For: {}   With level:{}'.format(
                msg.text,
                recipient,
                msg.level
                )
            )
