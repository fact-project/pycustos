import logging
import requests

from .base import Notifier

log = logging.getLogger(__name__)


class HTTPNotifier(Notifier):
    ''' A Notifier that sends http post request to a given url '''
    def __init__(self, auth=None, **kwargs):
        '''
        Create a new HTTPNotifier

        :param auth: If given, auth is handed over to request.post
        :param recipients: The urls to post to.

        :type recipients: Iterable of recipients or dict mapping categories to recipients
        :param categories: The message categories this Notifier should relay
        :type categories: Iterable
        :param level: The minimum level for messages to be relayed
        :type level: int
        '''
        self.auth = auth
        super().__init__(**kwargs)

    def notify(self, recipient,  msg):

        try:
            params = msg.to_dict()
            params.pop('image', None)
            ret = requests.post(recipient, params=params, auth=self.auth)
            ret.raise_for_status()
        except:
            log.exception('Could not post message')
