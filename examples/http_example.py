from custos import Custos, IntervalCheck, HTTPNotifier, levels
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

    console = HTTPNotifier(
        level=levels.INFO,
        recipients=['http://localhost:5000/messages'],
    )

    with Custos(checks=[hello_world], notifiers=[console]) as custos:
        custos.run()
