from custos import Custos, Message, IntervalCheck, ConsoleNotifier, levels
from time import sleep
import logging
from threading import Thread

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)


class MockCheck(IntervalCheck):
    ''' This check just sends a message each time its run. '''

    def check(self):
        # check whether condition fails or not
        self.queue.put(
            Message.info(
                'Hello Unit Test!',
            )
        )


def test_check_lifecycle():
    test_check_1 = MockCheck(interval=1)
    test_check_2 = MockCheck(interval=1.2)

    console = ConsoleNotifier(
        level=levels.INFO,
        recipients=['test_check_cycle'],
    )

    custos = Custos(
        checks=[test_check_1, test_check_2],
        notifiers=[console],
    )

    for check in custos.checks:
        assert not check.is_alive()

    t = Thread(target=custos.run)
    t.start()
    sleep(1)

    for check in custos.checks:
        assert check.is_alive()

    log.debug('Sleeping in main thread for 2 seconds')
    sleep(2)
    log.debug('Sleep finished')

    custos.stop()

    for check in custos.checks:
        assert check.stop_event.is_set()

    sleep(1)

    for check in custos.checks:
        assert not check.is_alive()
