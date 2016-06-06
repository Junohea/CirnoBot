from lib.database import CirnoDatabase
from datetime import datetime
from lib.utils import throttle

db = CirnoDatabase()


class CommandsDB(object):

    @throttle(5)
    def _cmd_stat(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Укажите пользователя!' % username)
            return
        data = '%s' % (db.getquantity(args))
        if int(data) < 1:
            cirno.sendmsg('%s: Не нашла сообщений от такого пользователя!'
                          % username)
        else:
            cirno.sendmsg('Количество сообщений от %s: %s' % (args, data))

    @throttle(5)
    def _cmd_q(self, cirno, username, args):
        randquot = db.getquote()
        if randquot:
            cirno.sendmsg('%s: %s' % (username, randquot))
        else:
            cirno.sendmsg('%s: Ничего не найдено!' % username)

    @throttle(5)
    def _cmd_pic(self, cirno, username, args):
        randpic = db.getpic()
        if randpic:
            cirno.sendmsg('%s: %s' % (username, randpic))
        else:
            cirno.sendmsg('%s: Ничего не найдено!' % username)

    @throttle(5)
    def _cmd_random(self, cirno, username, args):
        data = db.getrandom(args)
        if not data:
            cirno.sendmsg('%s: Не нашла такого пользователя!' % username)
        else:
            timestamp = datetime.fromtimestamp(data[0] / 1000) \
                .strftime('%d.%m.%Y %H:%M:%S')
            nick = data[1]
            quote = data[2]
            cirno.sendmsg('[%s] [%s] %s' % (timestamp, nick, quote))


def setup():
    return CommandsDB()
