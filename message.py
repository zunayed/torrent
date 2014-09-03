class Message(object):

    def __init__(self, length, msg, msg_type):
        self.length = length
        self.msg = msg
        self.msg_type = msg_type

    def checkLength(self):
        return self.length == len(self.msg)
