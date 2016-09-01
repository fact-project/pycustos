from custos import Custos, Message, IntervalCheck
import threading
from time import sleep


class TestCheck(IntervalCheck):
    ''' This check just sends a message each time its run. '''

    def check(self):
        #check whether condition fails or not
        self.queue.put(
            Message.info(
                'Hello, World!',
            )
        )

def test_stop_flag():

    test_check = TestCheck(interval=3)

    custos = Custos(
        checks=[test_check],
        notifiers=[],
    )
    print("asdasdasd")
    custos.run()
    sleep(500)
    # try:
    #     while True:
    #         sleep(10)
    # except (SystemExit, KeyboardInterrupt):
    #     custos.stop()
    #
    custos.stop()

if __name__ == '__main__':
    test_stop_flag()
