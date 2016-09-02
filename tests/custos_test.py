from custos import Custos, Message, IntervalCheck, ConsoleNotifier, levels
from time import sleep
import logging

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)

class MockCheck(IntervalCheck):
    ''' This check just sends a message each time its run. '''

    def check(self):
        #check whether condition fails or not
        self.queue.put(
            Message.info(
                'Hello Unit Test!',
            )
        )

def test_custos_lifecycle():
    test_check = MockCheck(interval=1)

    console = ConsoleNotifier(
        level=levels.INFO,
        recipients=['test_1'],
    )

    custos = Custos(
        checks=[test_check],
        notifiers=[console],
    )

    assert custos.is_alive() == False
    custos.start()

    assert custos.is_alive() == True

    log.debug('All Checks runnig')
    log.debug('Sleeping in main thread for 2 seconds')
    sleep(2)
    log.debug('Sleep finished')

    custos.stop()
    sleep(1)
    assert custos.stop_event.is_set()
    sleep(2)
    assert custos.is_alive() == False

if __name__ == '__main__':
    test_custos_lifecycle()
