from lib.utils import parsemedialink, checkrank
from time import sleep
from lib.gspreads import Googspread


class Gspread(object):
    gs = Googspread()

    def _cmd_db(self, cirno, username, data):
        if not data:
            cirno.sendmsg('%s: Укажите название и '
                          'серии (опционально).' % username)
        else:
            titles = self.gs.extenddata(data)
            pos = 'end'
            temp = True
            duration = 0
            if titles:
                for title in titles:
                    sleep(1)
                    x = parsemedialink(title)
                    cirno.addvideo(None, None, duration, temp, pos, x)
            else:
                cirno.sendmsg('%s: Ничего не нашла! Попробуй '
                              'посмотреть доступные'
                              ' тайтлы в хранилище.' % username)

    @checkrank(2)
    def _cmd_schedule(self, cirno, username, data):
        vids = self.gs.datashedule()[1:]
        pos = 'end'
        temp = True
        duration = 0
        for vid in vids:
            if vid:
                sleep(1)
                x = parsemedialink(vid)
                cirno.addvideo(None, None, duration, temp, pos, x)
            else:
                pass


def setup():
    return Gspread()
