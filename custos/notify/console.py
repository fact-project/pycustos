import logging

from .base import Notifier

log = logging.getLogger(__name__)


class ConsoleNotifier(Notifier):
    def notify(self, recipient, msg):
        log.info('Message: {}    For: {}'.format(msg.text, recipient))
