try:
    import telepot
    _has_telepot = True
except ImportError:
    _has_telepot = False

from io import BytesIO
import logging
import imghdr

from .base import Notifier


log = logging.getLogger(__name__)


class TelegramNotifier(Notifier):
    ''' A Notifier using the Telegram bot API via telepot '''
    def __init__(self, token, **kwargs):
        '''
        Create a new TelegramNotifier

        :param token: Your Bot's authentication token
        :param recipients: The chatIDs or usernames that should
                           be contacted by this Notifier

        :type recipients: Iterable of recipients or dict mapping categories to recipients
        :param categories: The message categories this Notifier should relay
        :type categories: Iterable
        :param level: The minimum level for messages to be relayed
        :type level: int
        '''
        if _has_telepot is False:
            raise ImportError('The telepot package is required for this Notifier')
        self.bot = telepot.Bot(token)
        super().__init__(**kwargs)

    def notify(self, recipient,  msg):
        try:
            self.bot.sendMessage(recipient, msg.text)
        except:
            log.exception('Could not send message')

        try:
            if msg.image:
                self.send_image(recipient, msg.image)
        except:
            log.exception('Could not send image')

    def send_image(self, chat_id, image):
        if isinstance(image, bytes):
            f = BytesIO(image)
            f.seek(0)
            extension = imghdr.what(f)
            self.bot.sendPhoto(chat_id, ('image.' + extension, f))

        elif isinstance(image, str):
            with open(image, 'rb') as f:
                self.bot.sendPhoto(chat_id, f)

        elif hasattr(image, 'read'):
            if hasattr(image, 'name'):
                self.bot.sendPhoto(chat_id, image)
            else:
                self.bot.sendPhoto(chat_id, ('image.png', image))

        else:
            raise TypeError(
                'image needs to be either a filename, bytes or file-like object'
            )
