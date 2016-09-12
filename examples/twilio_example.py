from custos import Custos, IntervalCheck, TwilioNotifier, levels
import logging

log = logging.getLogger('custos')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
log.addHandler(handler)

twilio_sid = '1234'
twilio_auth_token = 'abcd'
twilio_number = '+4912345'


class HelloWorldCheck(IntervalCheck):
    ''' This check just sends Hello World messages '''

    def check(self):
        self.info('Hello World')
        log.debug('message put into queue')


if __name__ == '__main__':
    log.debug('Example started')
    hello_world = HelloWorldCheck(interval=60)

    twilio = TwilioNotifier(
        twilio_sid, twilio_auth_token, twilio_number,
        ring_time=10,
        recipients=('+492345', ),
        level=levels.INFO,
    )

    with Custos(checks=[hello_world], notifiers=[twilio]) as custos:
        custos.run()
