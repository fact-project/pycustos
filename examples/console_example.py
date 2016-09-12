from custos import Custos, IntervalCheck, ConsoleNotifier, levels
import logging

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)


class HelloWorldCheck(IntervalCheck):
    ''' This check just sends Hello World messages '''

    def check(self):
        self.info('Hello, World!')


if __name__ == '__main__':
    hello_world = HelloWorldCheck(interval=5)

    console = ConsoleNotifier(
        level=levels.INFO,
        recipients=['Me', 'You', 'Hans'],
    )

    with Custos(checks=[hello_world], notifiers=[console]) as custos:
        custos.run()
