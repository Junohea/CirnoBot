from lib.database import CirnoDatabase
from datetime import datetime
from lib.utils import throttle, checkrank, check_picture
import re

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
            emotes_quantity = '%s' % (db.emotesquantity(args))
            ratio = int(emotes_quantity)*100/int(data)
            cirno.sendmsg('Количество сообщений от %s: %s. '
                          'Из них только со смайлами: %s. Смайлов от общего числа сообщений: %s%%'
                          % (args, data, emotes_quantity, round(ratio, 2)))

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

    @checkrank(2)
    def _cmd_save(self, cirno, username, args):
        if 'img class="chat-picture"' not in args:
            cirno.sendmsg('%s: Укажите ссылку на изображение.' % username)
            return
        matches = re.search('src="([^"]+)"', args)
        picture = matches.group(1)
        if check_picture(picture):
            pattern = re.compile('((https?://)?(i.imgur.com)+([^\?&#])+?[.](?:jpg|jpeg|png|bmp|gif))')
            if bool(pattern.match(picture)):
                   db.savepic(username, picture)
                   cirno.sendmsg('%s: Сохранила.' % username)
            else:
                cirno.sendmsg('%s: Разрешено сохранять изображения только с imgur.' % username)
        else:
            cirno.sendmsg('%s: Изображение не найдено.' % username)


def setup():
    return CommandsDB()
