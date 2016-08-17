from custos import Custos, IntervalCheck, SMTPNotifier, Message, levels
from time import sleep
import logging
from urllib.request import urlopen
from getpass import getpass

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)


class HelloWorldCheck(IntervalCheck):
    ''' This check just sends Hello World messages '''

    def check(self):
        self.queue.put(
            Message.info(
                'Hello, World!',
                image=urlopen('http://bellard.org/bpg/lena30.jpg'),
            )
        )


if __name__ == '__main__':
    hello_world = HelloWorldCheck(interval=30)

    recipients = []
    print('Please add your first recipient')
    while True:
        recipients.append(input('Email address: '))
        if not input('Add another recipient? [y,n]: ').lower().startswith('y'):
            break

    mail = SMTPNotifier(
        host='unimail.tu-dortmund.de',
        port=465,
        default_subject='Notifier Test',
        user=input('Unimail User: '),
        password=getpass('Unimail Password: '),
        sender='PyCustos <pycustos@local.host>',
        recipients=recipients,
        level=levels.INFO,
    )

    custos = Custos(
        checks=[hello_world],
        notifiers=[mail],
    )

    custos.start()
    log.debug('All Checks runnig')

    # keep main Thread alive:

    try:
        while True:
            sleep(10)
    except (SystemExit, KeyboardInterrupt):
        custos.stop()
