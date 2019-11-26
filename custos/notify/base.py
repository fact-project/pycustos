from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
import logging

from .levels import INFO


log = logging.getLogger(__name__)


class Notifier(metaclass=ABCMeta):
    '''
    The base class for all notifiers

    Notifiers are handling messages. Each notifier has a minimum level,
    recipients and categories.

    A notifier sends a message to each of the recipients if:
        * The categories of the message  in the categories of the notifier
        * The level of the message is equal or higher than the notifier's level

    Recipients can either be an iterable or a dict mapping categories to recipients
    '''
    def __init__(self, recipients, level=INFO, categories=None):
        self.recipients = recipients
        self.level = level
        self.categories = set(categories) if categories else None

    def handle_message(self, msg):
        if msg.level >= self.level:
            if self.categories is None or msg.category in self.categories:

                if isinstance(self.recipients, Mapping):
                    log.debug('Recipients is a Mapping')
                    recipients = self.recipients[msg.category]
                elif callable(self.recipients):
                    recipients = self.recipients(msg.category)
                else:
                    recipients = self.recipients



                for recipient in recipients:
                    try:
                        self.notify(recipient, msg)
                    except:
                        log.exception('Could not notifiy recipient {}'.format(recipient))

    @abstractmethod
    def notify(self, recipient, msg):
        pass
