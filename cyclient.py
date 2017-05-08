from lib.cirno import Cirno
from config import config
from socket import error as SocketError
from websocket import SSLError, WebSocketTimeoutException
from socketIO_client import SocketIO, WebsocketTransport, TimeoutError, ConnectionError
from socketIO_client.parsers import parse_packet_text
import requests


def patch_recv_packet(self):
    try:
        packet_text = self._connection.recv()
    except WebSocketTimeoutException as e:
        raise TimeoutError('recv timed out (%s)' % e)
    except SSLError as e:
        raise ConnectionError('recv disconnected by SSL (%s)' % e)
    except WebSocketConnectionClosedException as e:
        raise ConnectionError('recv disconnected (%s)' % e)
    except SocketError as e:
        raise ConnectionError('recv disconnected (%s)' % e)
    if not isinstance(packet_text, six.binary_type):
        packet_text = six.u(packet_text)
    engineIO_packet_type, engineIO_packet_data = parse_packet_text(
        packet_text)
    yield engineIO_packet_type, engineIO_packet_data

WebsocketTransport.recv_packet = patch_recv_packet


class Connections(object):
    def __init__(self):
        self.host = config['Server']['domain']
        self.channel = config['Server']['channel']
        self.channelpw = config['Server']['channelpass']
        self.name = config['Server']['login']
        self.password = config['Server']['password']

    def getsocketport(self):
        url = 'https://%s/socketconfig/%s.json' % (self.host, self.channel)
        req = requests.get(url).json()['servers']
        serv = [i['url'] for i in req if i['secure'] is True][0]
        port = int(serv[serv.rindex(':') + 1:])
        return port

    def cirnoconnect(self):
        with SocketIO('https://' + self.host, self.getsocketport(), Cirno, verify=False) as socketIO:
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
