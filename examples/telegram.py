from custos import NotifierPool, Check, TelegramNotifier, Message, levels
from queue import Queue
from time import sleep
import logging
from urllib.request import urlopen

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)

bot_token = ''


class HelloWorldCheck(Check):
    ''' This check just sends Hello World messages '''

    def check(self):
        self.queue.put(
            Message.info(
                'Hello Windows Users',
                image=urlopen('http://bellard.org/bpg/lena30.jpg'),
                category='Windows',
            )
        )
        self.queue.put(
            Message.info(
                'Hello Linux Users',
                image=urlopen('http://bellard.org/bpg/lena30.jpg'),
                category='Linux',
            )
        )
        log.debug('message put into queue')


if __name__ == '__main__':
    log.debug('Example started')
    message_queue = Queue()
    hello_world = HelloWorldCheck(interval=30, queue=message_queue)

    telegram = TelegramNotifier(
        bot_token,
        recipients={'Linux': [12345, 2131], 'Windows': [112321, -123123]},
        level=levels.INFO,
        categories={'Linux', 'Windows'},
    )

    pool = NotifierPool(
        message_queue,
        notifiers=(telegram, ),
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
