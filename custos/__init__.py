from queue import Empty, Queue
from threading import Event
import logging

from .checks import Check, IntervalCheck, ScheduledCheck
from .notify import Notifier
from .notify import TwilioNotifier
from .notify import SMTPNotifier
from .notify import Message
from .notify import levels
from .notify import TelegramNotifier
from .notify import ConsoleNotifier
from .notify import HTTPNotifier
from .notify import LogNotifier


log = logging.getLogger(__name__)


class Custos:
    '''
    The custos class holds checks and notifiers and sticks them together.

    Parameters
    ----------
    checks: list
        A list of Check instances
    notifiers: list
        A list of Notifier instances
    notify_on_exception: None or bool
        If not None, set notify_on_exception for all Checks
        This will result in messages with level ERROR and category 'check_error'
        if an exception occures during Check.check
    '''
    def __init__(self, checks, notifiers, notify_on_exception=None):
        self.queue = Queue()
        self.notifiers = notifiers
        self.checks = checks
        self.log = log.getChild(self.__class__.__name__)

        for check in self.checks:
            check.queue = self.queue
            if notify_on_exception is not None:
                check.notify_on_exception = notify_on_exception

        self.stop_event = Event()

    def start(self):
        for check in self.checks:
            check.start()

        self.log.info('%s running', self.__class__.__name__)

    def run(self):
        self.start()
        while not self.stop_event.is_set():
            try:
                message = self.queue.get(block=True, timeout=1)
            except Empty:
                continue

            for notifier in self.notifiers:
                try:
                    notifier.handle_message(message)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    self.log.exception(
                        '%s failed to handle message',
                        notifier.__class__.__name__
                    )

    def stop(self):
        for check in self.checks:
            check.stop()
        self.stop_event.set()
        self.log.info('%s stopped', self.__class__.__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
