from socketIO_client import SocketIO
from lib.cirno import Cirno
from conf import config


class Connections(object):
    def __init__(self):
        self.host = config['Server']['domain']
        self.port = int(config['Server']['port'])
        self.channel = config['Server']['channel']
        self.channelpw = config['Server']['channelpass']
        self.name = config['Server']['login']
        self.password = config['Server']['password']

    def cirnoconnect(self):
        with SocketIO(self.host, self.port, Cirno) as socketIO:
            socketIO.emit('initChannelCallbacks')
            socketIO.emit('joinChannel', {'name': self.channel,
                                          'pw': self.channelpw})
            socketIO.emit('login', {'name': self.name,
                                    'pw': self.password})
            socketIO.wait()


cirno = Connections()
cirno.cirnoconnect()
