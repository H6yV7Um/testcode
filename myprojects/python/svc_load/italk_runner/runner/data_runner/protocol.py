import msgpack

class Message(object):
    '''class doc'''
    def __init__(self, message_type, data, client_id):
        self.type = message_type
        self.data = data
        self.client_id = client_id

    def serialize(self):
        '''func doc'''
        return msgpack.dumps((self.type, self.data, self.client_id))

    @classmethod
    def unserialize(cls, data):
        '''func doc'''
        msg = cls(*msgpack.loads(data, encoding='utf-8'))
        return msg
