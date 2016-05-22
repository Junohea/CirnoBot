from lib.utils import parsemedialink, checkrank
from time import sleep
from lib.gspreads import Googspread


class Gspread(object):
    gs = Googspread()

    def _cmd_db(self, cirno, username, data):
        if not data:
            cirno.sendmsg(username + ': Укажите название'
                                     ' и серии (опционально).')
        else:
            titles = self.gs.frombase(data)
            pos = 'end'
            temp = True
            duration = 0
            if titles:
                for title in titles:
                    sleep(1)
                    x = parsemedialink(title)
                    cirno.addvideo(None, None, duration, temp, pos, x)

    @checkrank(2)
    def _cmd_schedule(self, cirno, username, data):
        vids = self.gs.datashedule()
        pos = 'end'
        temp = True
        duration = 0
        for vid in vids:
            sleep(1)
            x = parsemedialink(vid)
            cirno.addvideo(None, None, duration, temp, pos, x)


def setup():
    return Gspread()
