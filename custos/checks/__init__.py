from threading import Thread, Event
from abc import ABCMeta, abstractmethod
from apscheduler.schedulers.background import BlockingScheduler
import logging

log = logging.getLogger(__name__)


class Check(Thread, metaclass=ABCMeta):
    '''
    Abstract base class for checks.

    Subclasses need to implement the check method.
    This method has to push `Message` instance into
    the queue to notify that something has happend.

    All Exceptions in this occuring during the call of `check` are
    catched and logged.

    The thread has to be started with the .start() method,
    and will terminate after .stop() is called.
    '''
    def __init__(self, queue=None):
        self.queue = queue
        self.stop_event = Event()
        super().__init__()

    def stop(self):
        self.stop_event.set()

    def start(self):
        if self.queue is None:
            msg = (
                'queue not set. '
                'If you use a Check without the Custos class, you need to pass a Queue'
            )
            raise ValueError(msg)

        super().start()
        log.info('Check %s running', self.__class__.__name__)

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def run(self):
        pass


class IntervalCheck(Check, metaclass=ABCMeta):
    def __init__(self, interval=None, queue=None):
        self.interval = interval
        super().__init__(queue=queue)

    def run(self):
        while not self.stop_event.is_set():
            try:
                self.check()
            except Exception as e:
                log.exception('Exception while running check')
            self.stop_event.wait(self.interval)

        log.info('Check %s stopped', self.__class__.__name__)


class ScheduledCheck(Check, metaclass=ABCMeta):
    def __init__(self, scheduler_args, queue=None):
        super().__init__(queue=queue)

        self.scheduler = BlockingScheduler(
            job_defaults={'misfire_grace_time': 5*60}
        )
        self.scheduler.add_job(self.check, **scheduler_args)

    def run(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()
