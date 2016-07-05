from threading import Thread, Event
from abc import ABCMeta, abstractmethod
import logging

log = logging.getLogger(__name__)


class Check(Thread, metaclass=ABCMeta):
    '''
    base class for checks

    Subclasses need to implement the check method.
    This method has to push `Message` instance into
    the queue to notify that something has happend.

    All Exceptions in this occuring during the call of `check` are
    catched and logged.

    The thread has to be started with the .start() method,
    and will terminate after .stop() is called.
    '''
    def __init__(self, queue, interval):
        self.queue = queue
        self.interval = interval
        self.stop_event = Event()

        super(Check, self).__init__()

    def run(self):
        while not self.stop_event.is_set():
            try:
                self.check()
            except Exception as e:
                log.exception('Exception while running check')
            self.stop_event.wait(self.interval)

    def stop(self):
        self.stop_event.set()

    @abstractmethod
    def check(self):
        pass