from custos import NotifierPool, Check, TwilioNotifier, Message, levels
from queue import Queue
from time import sleep
import logging

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)

twilio_sid = '1234'
twilio_auth_token = 'abcd'
twilio_number = '+4912345'


class HelloWorldCheck(Check):
    ''' This check just sends Hello World messages '''

    def check(self):
        self.queue.put(Message.info('Hello World'))
        log.debug('message put into queue')


if __name__ == '__main__':
    log.debug('Example started')
    message_queue = Queue()
    hello_world = HelloWorldCheck(interval=60, queue=message_queue)

    twilio = TwilioNotifier(
        '+4978910',
        twilio_sid, twilio_auth_token, twilio_number,
        level=levels.INFO,
        ring_time=10,
    )

    pool = NotifierPool(
        message_queue,
        notifiers=(twilio, ),
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
