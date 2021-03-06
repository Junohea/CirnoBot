import requests
from lib.utils import throttle
from random import choice


class Twochannel(object):

    def boardlist(self):
        getboards = 'https://2ch.hk/makaba/mobile.fcgi?task=get_boards'
        try:
            data = requests.get(getboards).json()
            boards = ['Политика', 'Пользовательские', 'Тематика',
                      'Техника и софт', 'Разное', 'Творчество',
                      'Игры', 'Японская культура', 'Взрослым']
        except Exception:
            return
        result = [x['id'] for i in boards for x in data[boards[boards.index(i)]]]
        return result

    def managethreads(self, board):
        inboard = 'https://2ch.hk/%s/index.json' % board
        threads = requests.get(inboard).json()['threads']
        result = [i['thread_num'] for i in threads]
        return result

    def serfthread(self, board, managethreads):
        try:
            inthread = 'https://2ch.hk/%s/res/%s.json' \
                       % (board, choice(managethreads))
            getthread = requests.get(inthread).json()['threads'][0]['posts']

        except Exception:
            return
        return getthread

    def get2chpic(self, board):
        managethreads = self.managethreads(board)
        if managethreads is None:
            return
        try:
            inthread = self.serfthread(board, managethreads)
            result = ['https://2ch.hk%s' %
                      (i['files'][0]['path']) for
                      i in inthread if len(i['files']) != 0 and
                      i['files'][0]['type'] in [1, 2]]
        except Exception:
            return
        return choice(result) if result else 'Ничего не найдено!'

    @throttle(8)
    def _cmd_2ch(self, cirno, username, args):
        if args not in self.boardlist() or args in cirno.disallowed2ch:
            cirno.sendmsg('%s: Доска отсутствует, либо запрещена.' % username)
        else:
            randpic = self.get2chpic(args)
            if randpic:
                cirno.sendmsg('%s: %s' % (username, randpic))


def setup():
    return Twochannel()
