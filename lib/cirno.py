from socketIO_client import BaseNamespace
from lib.database import CirnoDatabase
from time import time
from lib.utils import filterchat
import codecs
import json
import importlib
import os
from config import config


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
        self.userdict = {}
        self.cmdthrottle = {}
        self.settings = {
            'disallow': []
        }
        self.updatesettings()
        self.what = config['Misc']['errorpic']
        self.name = config['Server']['login']
        self.mod = config['Server']['modflair']
        self.rus_commands = config['Misc']['rus_commands']
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
                    self.triggers['commands'][trigger] \
                        = getattr(instance, method)
        return self.triggers

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
                and username not in self.settings['disallow']:
            return self.handle(self, username, msg)

        self.db.insertchat(timestamp, username, msg)

    def on_pm(self, data):
        username = data['username']
        msg = data['msg']
        rank = self.db.getuserrank(username)

        msg = filterchat(msg)
        if msg is None:
            return

        if rank >= 2:
            self.handle(self, username, msg)

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

    def on_userLeave(self, data):
        del self.userdict[data['name']]

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

    def updatesettings(self):
        try:
            self.settings = self.readsettings()
        except:
            self.writesettings()

    def writesettings(self):
        with codecs.open('settings.json', 'w', 'utf8') as f:
            f.write(json.dumps(self.settings, ensure_ascii=False))

    def readsettings(self):
        data = codecs.open('settings.json', 'r', 'utf-8')
        result = json.load(data)
        return result

    def ruscommands(self):
        commandslist = self.loadplugins()
        ruscommandsdict = {
            "выбор": commandslist['commands'].get("pick", None),
            "ролл": commandslist['commands'].get("roll", None),
            "спросить": commandslist['commands'].get("ask", None),
            "кто": commandslist['commands'].get("who", None),
            "аптайм": commandslist['commands'].get("uptime", None),
            "цитата": commandslist['commands'].get("quote", None),
            "погода": commandslist['commands'].get("weather", None),
            "курс": commandslist['commands'].get("rate", None),
            "переведи": commandslist['commands'].get("translate", None),
            "добавь": commandslist['commands'].get("add", None),
            "рандом": commandslist['commands'].get("random", None),
            "статистика": commandslist['commands'].get("stat", None),
            "пни": commandslist['commands'].get("hit", None),
            "загугли": commandslist['commands'].get("search", None),
            "q": commandslist['commands'].get("q", None),
            "пик": commandslist['commands'].get("pic", None),
            "booru": commandslist['commands'].get("booru", None),
            "4chan": commandslist['commands'].get("4chan", None),
            "2ch": commandslist['commands'].get("2ch", None),
            "алерт": commandslist['commands'].get("alert", None),
            "запрети": commandslist['commands'].get("deny", None),
            "разреши": commandslist['commands'].get("allow", None),
        }
        return ruscommandsdict

    def handle(self, cirno, username, msg):
        commandslist = self.loadplugins()
        splice = msg.split(' ')
        command = splice.pop(0)[1:]
        args = ' '.join("%s" % x for x in splice).strip()
        if self.rus_commands:
            method = self.ruscommands().get(command, None)
        else:
            method = commandslist['commands'].get(command, None)
        if method:
            try:
                return method(cirno, username, args)
            except:
                if cirno.what:
                    cirno.sendmsg("%s: %s" % (username, cirno.what))
                else:
                    return
        else:
            return
