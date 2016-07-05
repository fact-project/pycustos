import telepot
from io import BytesIO
import logging

from .base import Notifier


log = logging.getLogger(__name__)


class TelegramNotifier(Notifier):
    def __init__(self, token, chat_ids, **kwargs):

        self.bot = telepot.Bot(token)
        self.chat_ids = list(chat_ids)

        super().__init__(**kwargs)

    def notify(self, msg):
        for chat_id in self.chat_ids:

            try:
                self.bot.sendMessage(chat_id, msg.text)
            except:
                log.exception('Could not send message')

            try:
                if msg.image:
                    self.send_image(chat_id, msg.image)
            except:
                log.exception('Could not send image')

    def send_image(self, chat_id, image):
        if isinstance(image, bytes):
            f = BytesIO(image)
            f.seek(0)
            self.bot.sendPhoto(chat_id, ('image.png', f))

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
