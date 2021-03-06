from lib.database import CirnoDatabase
from datetime import datetime
from lib.utils import throttle, checkrank, check_picture, check_url
import re

db = CirnoDatabase()


class CommandsDB(object):
    @throttle(5)
    def _cmd_stat(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Specify a user!' % username)
            return
        data = '%s' % (db.getquantity(args))
        if int(data) < 1:
            cirno.sendmsg('%s: No messages from this user were found!'
                          % username)
        else:
            emotes_quantity = '%s' % (db.emotesquantity(args))
            ratio = int(emotes_quantity) * 100 / int(data)
            cirno.sendmsg('Number of messages from %s: %s. '
                          'Of these, only with smiles(?): %s. Smile from the total number of messages(?): %s%%'
                          % (args, data, emotes_quantity, round(ratio, 2)))

    @throttle(5)
    def _cmd_q(self, cirno, username, args):
        randquot = db.getquote()
        if randquot:
            cirno.sendmsg('%s: %s' % (username, randquot))
        else:
            cirno.sendmsg('%s: Nothing found!' % username)

    @throttle(5)
    def _cmd_pic(self, cirno, username, args):
        randpic = db.getpic()
        if randpic:
            cirno.sendmsg('%s: %s' % (username, randpic))
        else:
            cirno.sendmsg('%s: Nothing found!' % username)

    @throttle(5)
    def _cmd_random(self, cirno, username, args):
        data = db.getrandom(args)
        if not data:
            cirno.sendmsg("%s: I didn't find this user!" % username)
        else:
            timestamp = datetime.fromtimestamp(data[0] / 1000) \
                .strftime('%d.%m.%Y %H:%M:%S')
            nick = data[1]
            quote = data[2]
            cirno.sendmsg('[%s] [%s] %s' % (timestamp, nick, quote))

    @checkrank(2)
    def _cmd_save(self, cirno, username, args):
        if check_url(args) is False:
            cirno.sendmsg('%s: Please provide a link to the image.' % username)
            return

        if check_picture(args):
            pattern = re.compile('((https?://)?(i.imgur.com)+([^\?&#])+?[.](?:jpg|jpeg|png|bmp|gif))')
            if bool(pattern.match(args)):
                db.savepic(username, args)
                cirno.sendmsg('%s: Saving.' % username)
            else:
                cirno.sendmsg('%s: Only allowed to save from imgur.' % username)
        else:
            cirno.sendmsg('%s: Image not found.' % username)


def setup():
    return CommandsDB()
