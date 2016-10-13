from socketIO_client import BaseNamespace
from lib.database import CirnoDatabase
from lib.utils import *
from lib.commands import *
from config import config


class Cirno(BaseNamespace):
    def __init__(self, io, path):
        super().__init__(io, path)
        self.db = CirnoDatabase()
        self.starttime = int(time.time() * 1000)
        self.cirnostart = time.time()
        self.userdict = {}
        self.cmdthrottle = {}
        self.settings = {'disallow': []}
        self.channelOpts = {}
        loadplugins()
        updatesettings(self)
        self.allowed_sources = config['Misc']['allowed_sources']
        self.what = config['Misc']['errorpic']
        self.name = config['Server']['login']
        self.mod = config['Server']['modflair']
        self.disallowed2ch = config['API']['disallow_2ch_boards'].split()
        self.disallowed4ch = config['API']['disallow_4chan_boards'].split()

    def on_chatMsg(self, data):
        username = data['username']
        msg = data['msg']
        timestamp = data['time']
        meta = data['meta']

        if username == '[server]':
            return

        msg = filterchat(msg)
        if msg is None:
            return

        if timestamp < self.starttime:
            return

        if msg.startswith('!') \
                and 'shadow' not in meta \
                and username not in readsettings()["disallow"]:
            return handle(self, username, msg)

        self.db.insertchat(timestamp, username, msg)

    def on_pm(self, data):
        username = data['username']
        msg = data['msg']
        rank = self.db.getuserrank(username)

        msg = filterchat(msg)
        if msg is None:
            return

        if rank >= 2:
            handle(self, username, msg)

    def on_addUser(self, data):
        name = data['name']
        rank = data['rank']
        afk = data['meta']['afk']
        self.userdict[name] = {
            'rank': rank,
            'afk': afk
        }
        self.db.insertuser(name, rank)
        self.db.insertuserrank(name, rank)

    def on_channelOpts(self, data):
        self.channelOpts = data

    def on_userLeave(self, data):
        del self.userdict[data['name']]
        rank_list = [value['rank'] for key, value in self.userdict.items() if key != 'Сырно']
        if [2, 3, 5, 255] not in rank_list:
            self.emit('setOptions', {'allow_voteskip': True})

    def on_userlist(self, data):
        for i in data:
            self.userdict[i['name']] = {
                'rank': i['rank'],
                'afk': i['meta']['afk']
            }

    def on_setAFK(self, data):
        username = data['name']
        afk = data['afk']
        if username and data:
            self.userdict[username]['afk'] = afk

    def openpoll(self, data):
        self.emit('newPoll', data)

    def sendmsg(self, message):
        rank = self.db.getuserrank(self.name)
        if self.mod:
            self.emit('chatMsg',
                      {'msg': message,
                       'meta': {
                           "modflair": rank
                       }
                       })
        else:
            self.emit('chatMsg',
                      {'msg': message,
                       'meta': {}
                       })

    def handle_voteskip(self):
        if self.channelOpts['allow_voteskip']:
            self.emit('setOptions', {'allow_voteskip': False})
        else:
            self.emit('setOptions', {'allow_voteskip': True})

    def addvideo(self, typev, idv, duration, temp, pos, link):
        if link:
            json = {
                'id': link['id'],
                'type': link['type'],
                'pos': pos,
                'duration': duration,
                "temp": temp
            }
            self.emit("queue", json)
        else:
            json = {
                'id': idv,
                'type': typev,
                'pos': pos,
                'duration': duration,
                "temp": temp
            }
            self.emit("queue", json)
