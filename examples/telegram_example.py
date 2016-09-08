from custos import Custos, IntervalCheck, TelegramNotifier, levels
import logging
from urllib.request import urlopen

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)


class HelloWorldCheck(IntervalCheck):
    ''' This check just sends Hello World messages '''

    def check(self):
        self.info(
            'Hello Windows Users',
            image=urlopen('http://bellard.org/bpg/lena30.jpg'),
            category='Windows',
        )
        self.info(
            'Hello Linux Users',
            image=urlopen('http://bellard.org/bpg/lena30.jpg'),
            category='Linux',
        )


if __name__ == '__main__':
    log.debug('Example started')
    hello_world = HelloWorldCheck(interval=30)

    telegram = TelegramNotifier(
        token=input('Telegram Bot Token: ').strip(),
        recipients={'Linux': [12345, 2131], 'Windows': [112321, -123123]},
        level=levels.INFO,
        categories={'Linux', 'Windows'},
    )

    custos = Custos(
        checks=[hello_world],
        notifiers=[telegram],
    )

    with Custos(checks=[hello_world], notifiers=[telegram]) as custos:
        custos.run()
