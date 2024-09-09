
class Log(object):
    def __init__(
            self,
            subject,
            object,
            timestamp,
            content
    ):
        self.subject = subject
        self.object = object
        self.timestamp = timestamp
        self.content = content