import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import mimetypes
import imghdr
from io import BytesIO
import os
import logging

from .base import Notifier


log = logging.getLogger(__name__)


class SMTPNotifier(Notifier):
    def __init__(self, host, port, user, password, sender, default_subject, **kwargs):
        self.sender = sender
        self.default_subject = default_subject
        self.server = smtplib.SMTP_SSL(host, port)
        self.server.login(user, password)
        super().__init__(**kwargs)

    def notify(self, recipient, msg):
        mail = MIMEMultipart()
        mail['Subject'] = msg.title if msg.title else self.default_subject
        mail['From'] = self.sender
        mail['To'] = recipient

        mail.attach(MIMEText(msg.text, 'plain'))

        if msg.image is not None:
            if isinstance(msg.image, bytes):
                image_data = BytesIO(msg.image)
                image_data.seek(0)
                extension = imghdr.what(image_data)
                filename = 'image.' + extension

            elif isinstance(msg.image, str):
                with open(msg.image, 'rb') as f:
                    image_data = BytesIO(f.read())
                image_data.seek(0)
                filename = msg.image

            elif hasattr(msg.image, 'read'):
                image_data = BytesIO(msg.image.read())
                image_data.seek(0)

                if hasattr(msg.image, 'name'):
                    filename = os.path.basename(msg.image.name)
                else:
                    extension = imghdr.what(image_data)
                    filename = 'image.' + extension

            ctype, encoding = mimetypes.guess_type(filename)
            maintype, subtype = ctype.split('/')
            att = MIMEImage(image_data.read(), _subtype=subtype)

            att.add_header('Content-Disposition', 'attachment', filename=filename)
            mail.attach(att)

        self.server.sendmail(
            from_addr=self.sender,
            to_addrs=recipient,
            msg=mail.as_string(),
        )
        log.debug('Send mail to {}'.format(recipient))
