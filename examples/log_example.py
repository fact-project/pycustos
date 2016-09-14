from custos import Custos, IntervalCheck, LogNotifier, levels
import logging
FORMAT='%(asctime)s - %(levelname)s - %(name)s | %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class HelloWorldCheck(IntervalCheck):
    ''' This check just sends Hello World messages '''

    def check(self):
        self.info('Hello, World!')


class WarningCheck(IntervalCheck):
    ''' This check just sends a warning '''

    def check(self):
        self.warning('Winter is coming!')


if __name__ == '__main__':
    hello_world = HelloWorldCheck(interval=5)
    winter = WarningCheck(interval=7)

    log_notify = LogNotifier(
        level=levels.DEBUG,
        recipients=['Me', 'You', 'Hans'],
    )

    with Custos(checks=[hello_world, winter], notifiers=[log_notify]) as custos:
        custos.run()
