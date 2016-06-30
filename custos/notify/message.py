from .levels import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Message:
    def __init__(self, text, level=INFO, image=None, categories=None):
        self.level = level
        self.text = text
        self.image = image

    @classmethod
    def debug(cls, *args, **kwargs):
        return cls(*args, level=DEBUG, **kwargs)

    @classmethod
    def info(cls, *args, **kwargs):
        return cls(*args, level=INFO, **kwargs)

    @classmethod
    def warning(cls, *args, **kwargs):
        return cls(*args, level=WARNING, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs):
        return cls(*args, level=ERROR, **kwargs)

    @classmethod
    def critical(cls, *args, **kwargs):
        return cls(*args, level=CRITICAL, **kwargs)
