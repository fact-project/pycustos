from threading import Thread, Event
from abc import ABCMeta, abstractmethod
from apscheduler.schedulers.background import BlockingScheduler
import logging
from traceback import format_exc

from ..notify.message import Message
from ..notify.levels import DEBUG, INFO, WARNING, ERROR, CRITICAL

log = logging.getLogger(__name__)


class Check(Thread, metaclass=ABCMeta):
    '''
    Abstract base class for checks.

    Subclasses need to implement the check method.
    This method has to push `Message` instance into
    the queue to notify that something has happend.

    All Exceptions in this occuring during the call of `check` are
    catched and logged.
    If notify_on_exception is True, also a message with category check_error
    and level error will be pushed into the message queue.

    The thread has to be started with the .start() method,
    and will terminate after .stop() is called.
    '''
    def __init__(self, queue=None, notify_on_exception=True):
        self.queue = queue
        self.log = log.getChild(self.__class__.__name__)
        self.notify_on_exception = notify_on_exception
        super().__init__()

    def start(self):
        if self.queue is None:
            msg = (
                'queue not set. '
                'If you use a Check without the Custos class, you need to pass a Queue'
            )
            raise ValueError(msg)

        super().start()
        self.log.info('Check %s running', self.__class__.__name__)

    def message(self, *args, **kwargs):
        self.queue.put(
            Message(*args, check=self.__class__.__name__, **kwargs)
        )

    def debug(self, *args, **kwargs):
        self.message(*args, level=DEBUG, **kwargs)

    def info(self, *args, **kwargs):
        self.message(*args, level=INFO, **kwargs)

    def warning(self, *args, **kwargs):
        self.message(*args, level=WARNING, **kwargs)

    def error(self, *args, **kwargs):
        self.message(*args, level=ERROR, **kwargs)

    def critical(self, *args, **kwargs):
        self.message(*args, level=CRITICAL, **kwargs)

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def run(self):
        pass


class IntervalCheck(Check, metaclass=ABCMeta):
    '''
    Abstract base class for a check that runs every interval seconds

    Child classes need to implement the check method.
    '''
    def __init__(self, interval=None, queue=None):
        self.interval = interval
        self.stop_event = Event()
        super().__init__(queue=queue)

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            try:
                self.check()
            except Exception as e:
                if self.notify_on_exception:
                    self.error(
                        'Exception while running check. Traceback:\n {}'.format(
                            format_exc()
                        ),
                        category='check_error',
                    )
                log.exception('Exception while running check')
            self.stop_event.wait(self.interval)

        self.log.info('Check %s stopped', self.__class__.__name__)


class ScheduledCheck(Check, metaclass=ABCMeta):
    '''
    An abstract base class for a check that runs based on
    the Scheduler from apscheduler

    Child classes need to implement the check method
    '''
    def __init__(self, queue=None, **kwargs):
        '''
        Create a new instance of this Check
        The kwargs are handed over to apscheduler.blocking.BlockingScheduler.add_job
        and decide when the checks are run. For example `trigger='cron', hour=8` will
        run this check every day at 8 o'clock
        '''
        super().__init__(queue=queue)

        self.scheduler = BlockingScheduler(
            job_defaults={'misfire_grace_time': 5*60}
        )
        self.scheduler.add_job(self.check, **kwargs)

    def run(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()
        self.log.info('Check %s stopped', self.__class__.__name__)
