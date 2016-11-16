import logging

from .base import Notifier

log = logging.getLogger(__name__)


class LogNotifier(Notifier):
    '''
    A simple notifier class to log notifications.
    '''
    def notify(self, recipient, msg):
        log.log(
            msg.level,
            'Check: {} - Message: {}'.format(
                msg.check,
                msg.text,
            )
        )
