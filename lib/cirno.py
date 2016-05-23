from socketIO_client import BaseNamespace
from lib.database import CirnoDatabase
from time import time
from lib.utils import filterchat
import importlib
import os
from conf import config


def importplugins(path):
    files = os.listdir(path)
    importpath = path.replace('/', '.')
    modulenames = [importpath + i[:-3] for i in files
                   if not i.startswith('_') and i.endswith('.py')]
    modules = list(map(importlib.import_module, modulenames))
    return modules


class Cirno(BaseNamespace):
    def __init__(self, io, path):
        super().__init__(io, path)
        self.db = CirnoDatabase()
        self.starttime = int(time() * 1000)
        self.cirnostart = time()
        self.loadplugins()
        self.userlist = {}
        self.afklist = {}
        self.triggers = {}
        self.what = ': http://tehtube.tv/img/neponyala.jpg'
        self.name = config['Server']['login']
        self.mod = config['Server']['modflair']
        self.disallowed2ch = config['API']['disallow_2ch_boards'].split()
        self.disallowed4ch = config['API']['disallow_4chan_boards'].split()

    def loadplugins(self):
        modules = importplugins('cmds/')
        self.triggers = {'commands': {}}
        for module in modules:
            instance = module.setup()
            for method in dir(instance):
                if method.startswith('_cmd_'):
                    trigger = '%s' % method[5:]
                    self.triggers['commands'][trigger]\
                        = getattr(instance, method)
        return self.triggers

    def on_chatMsg(self, data):
        username = data['username']
        msg = data['msg']
        timestamp = data['time']

        if username == '[server]':
            return

        msg = filterchat(msg)
        if msg is None:
            return

        if timestamp < self.starttime:
            return

        if msg.startswith('!'):
            return self.handle(self, username, msg)

        self.db.insertchat(timestamp, username, msg)

    def on_pm(self, data):
        username = data['username']
        msg = data['msg']
        rank = self.db.getuserrank(username)
        if rank >= 2:
            self.handle(self, username, msg)

    def on_addUser(self, data):
        name = data['name']
        rank = data['rank']
        self.userlist[name] = rank
        self.db.insertuser(name, rank)
        self.db.insertuserrank(name, rank)

    def on_userLeave(self, data):
        user = data['name']
        del self.userlist[user]
        if user in self.afklist:
            del self.afklist[user]

    def on_updatePoll(self, data):
        if data['initiator'] != self.name:
            return
        count = data['counts']
        title = data['title'].replace('Ставим оценку ', '')
        if '?' in "%s" % count[0] or sum(count) == 0:
            return
        else:
            count.insert(0, 0)
            q = [count[i] * i for i in range(len(count))]
            if sum(q) == 1:
                return
            rating = float(sum(q[2:])) / sum(count[2:])
            self.sendmsg('Оценка {}: {}'.format(title, round(rating, 2)))

    def on_userlist(self, data):
        for i in data:
            self.userlist[i['name']] = i['rank']
            self.afklist[i['name']] = i['meta']['afk']

    def on_setAFK(self, data):
        self.afklist[data['name']] = data['afk']

    def openpoll(self, data):
        self.emit('newPoll', data)

    def endpoll(self):
        self.emit('closePoll')

    def sendpm(self, username, msg):
        self.emit('pm', {
            'to': username,
            'msg': msg,
            'meta': {}
        })

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

    def handle(self, cirno, username, msg):
        commandslist = self.loadplugins()
        splice = msg.split(' ')
        command = splice.pop(0)[1:]
        args = ' '.join("%s" % x for x in splice).strip()
        method = commandslist['commands'].get(command, None)
        if method:
            try:
                return method(cirno, username, args)
            except:
                cirno.sendmsg(username + cirno.what)
        else:
            return
