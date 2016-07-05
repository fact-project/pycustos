from custos import NotifierPool, Check, SMTPNotifier, Message, levels
from queue import Queue
from time import sleep
import logging
from urllib.request import urlopen
from getpass import getpass

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)

recipients = []


class HelloWorldCheck(Check):
    ''' This check just sends Hello World messages '''

    def check(self):
        self.queue.put(
            Message.info(
                'Hello, World!',
                image=urlopen('http://bellard.org/bpg/lena30.jpg'),
            )
        )
        log.debug('message put into queue')


if __name__ == '__main__':
    log.debug('Example started')
    message_queue = Queue()
    hello_world = HelloWorldCheck(interval=30, queue=message_queue)

    mail = SMTPNotifier(
        host='unimail.tu-dortmund.de',
        port=465,
        default_subject='Notifier Test',
        user=input('Unimail User:'),
        password=getpass('Unimail Password: '),
        sender='PyCustos',
        recipients=recipients,
        level=levels.INFO,
    )

    pool = NotifierPool(
        message_queue,
        notifiers=(mail, ),
    )

    hello_world.start()
    pool.start()
    log.debug('All Checks runnig')

    # keep main Thread alive:

    try:
        while True:
            sleep(10)
    except (SystemExit, KeyboardInterrupt):
        hello_world.stop()
        pool.stop()
