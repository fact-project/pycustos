from queue import Empty
from threading import Thread, Event
import logging


logger = logging.getLogger(__name__)


class NotifierPool(Thread):
    '''
    A pool of notifiers. The NotifierPool waits for
    '''
    def __init__(self, queue, notifiers):
        self.queue = queue
        self.notifiers = notifiers
        self.stop_event = Event()

        super(NotifierPool, self).__init__()

    def run(self):
        while not self.stop_event.is_set():
            try:
                message = self.queue.get(block=True, timeout=1)
            except Empty:
                continue

            for notifier in self.notifiers:
                try:
                    notifier.handle_message(message)
                except:
                    logger.exception('{} failed to handle message'.format(
                        notifier.__class__.__name__
                    ))

    def stop(self):
        self.stop_event.set()
