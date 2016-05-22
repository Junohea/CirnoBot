from re import sub
from time import sleep
from lib.utils import parsemedialink


class Addvideo(object):

    def _cmd_add(self, cirno, username, data):
        if not data:
            cirno.sendmsg(username + ': Укажите как минимум один ролик.')
        else:
            pos = 'end'
            temp = True
            duration = 0
            data = sub(r'<[^>]+>', '', data)
            vidlist = data.split(' ')
            for vid in vidlist:
                sleep(1)
                x = parsemedialink(vid)
                cirno.addvideo(None, None, duration, temp, pos, x)


def setup():
    return Addvideo()
