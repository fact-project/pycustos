from datetime import datetime
from .levels import INFO


class Message:
    def __init__(self, text, level=INFO, check=None, image=None, title=None, category='default'):
        self.timestamp = datetime.utcnow()
        self.level = level
        self.text = text
        self.image = image
        self.title = title
        self.category = category
        self.check = check

    def to_dict(self):
        return {
            'level': self.level,
            'timestamp': self.timestamp,
            'text': self.text,
            'title': self.title,
            'category': self.category,
            'image': self.image,
            'check': self.check,
        }
