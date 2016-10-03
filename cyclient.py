from socketIO_client import SocketIO
from lib.cirno import Cirno
from config import config
import requests


class Connections(object):
    def __init__(self):
        self.host = config['Server']['domain']
        self.channel = config['Server']['channel']
        self.channelpw = config['Server']['channelpass']
        self.name = config['Server']['login']
        self.password = config['Server']['password']

    def getsocketport(self):
        url = 'http://%s/socketconfig/%s.json' % (self.host, self.channel)
        req = requests.get(url).json()['servers']
        serv = [i['url'] for i in req if i['secure'] is False][0]
        port = int(serv[serv.rindex(':') + 1:])
        return port

    def cirnoconnect(self):
        with SocketIO(self.host, self.getsocketport(), Cirno, transports='xhr-polling') as socketIO:
            socketIO.emit('initChannelCallbacks')
            socketIO.emit('joinChannel', {'name': self.channel,
                                          'pw': self.channelpw})
            socketIO.emit('login', {'name': self.name,
                                    'pw': self.password})
            socketIO.wait()


def start():
    cirno = Connections()
    cirno.cirnoconnect()

if __name__ == '__main__':
    start()
