from lib.database import CirnoDatabase
from datetime import datetime

db = CirnoDatabase()


class CommandsDB(object):

    def _cmd_stat(self, cirno, username, args):
        if not args:
            cirno.sendmsg(username + ': Укажите пользователя!')
            return
        data = "%s" % (db.getquantity(args))
        if int(data) < 1:
            cirno.sendmsg(username + ': Не нашла сообщений от'
                                     ' такого пользователя!')
        else:
            cirno.sendmsg("Количество сообщений от " + args + ": " + data)

    def _cmd_q(self, cirno, username, args):
        randquot = db.getquote()
        if randquot:
            cirno.sendmsg(username + ': ' + randquot)

    def _cmd_pic(self, cirno, username, args):
        randpic = db.getpic()
        if randpic:
            cirno.sendmsg(username + ': ' + randpic)

    def _cmd_random(self, cirno, username, args):
        data = db.getrandom(args)
        if not data:
            cirno.sendmsg(username + ': Не нашла такого пользователя!')
        else:
            timestamp = datetime.fromtimestamp(data[0] / 1000) \
                .strftime('%d.%m.%Y %H:%M:%S')
            nick = data[1]
            quote = data[2]
            cirno.sendmsg('[' + timestamp + '] [' + nick + '] ' + quote)


def setup():
    return CommandsDB()
