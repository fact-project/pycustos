import logging

from .base import Notifier

log = logging.getLogger(__name__)


class ConsoleNotifier(Notifier):
    def notify(self, recipient, msg):
        if msg.level == logging.INFO:
            log.info('Message: {}    For: {}'.format(msg.text, recipient))
        if msg.level == logging.DEBUG:
            log.debug('Message: {}    For: {}'.format(msg.text, recipient))
        if msg.level == logging.WARN:
            log.warn('Message: {}    For: {}'.format(msg.text, recipient))
        if msg.level == logging.CRITICAL:
            log.critical('Message: {}    For: {}'.format(msg.text, recipient))
        if msg.level == logging.ERROR:
            log.error('Message: {}    For: {}'.format(msg.text, recipient))
