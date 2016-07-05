try:
    from twilio.rest import TwilioRestClient
    _has_twilio = True
except ImportError:
    _has_twilio = False

from urllib.parse import urlencode
from .base import Notifier
import logging


log = logging.getLogger(__name__)


def build_url(url, params):
    return url + '?' + urlencode(params)


echo_url = 'http://twimlets.com/echo'
message_url = 'http://twimlets.com/message'

hangup_twiml = '''<Response>
  <Hangup>
</Response>
'''
hangup_url = build_url(echo_url, {'Twiml': hangup_twiml})


class TwilioNotifier(Notifier):
    def __init__(
            self,
            sid,
            auth_token,
            twilio_number,
            ring_time=30,
            twiml='message',
            **kwargs
            ):

        if _has_twilio is False:
            raise ImportError('The twilio package is required for this Notifier')

        self.client = TwilioRestClient(sid, auth_token)
        self.twilio_number = twilio_number
        self.ring_time = ring_time
        self.twiml = 'message'

        super().__init__(**kwargs)

    def place_call(self, number, url):

        self.call = self.client.calls.create(
            url=url,
            to=number,
            from_=self.twilio_number,
            timeout=self.ring_time,
        )

    def notify(self, recipient,  msg):
        log.debug('Received message')
        if self.twiml == 'message':
            url = build_url(message_url, {'Message': msg.text})

        elif self.twiml == 'hangup':
            url = hangup_url

        else:
            url = build_url(echo_url, {'Twiml': self.twiml})

        log.debug('Placing call')
        self.place_call(recipient, url)
