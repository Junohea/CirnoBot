import requests
from random import choice


class Twochannel(object):

    def boardlist(self):
        getboards = 'https://2ch.hk/makaba/mobile.fcgi?task=get_boards'
        try:
            data = requests.post(getboards)
            boards = ['Политика', 'Пользовательские', 'Тематика',
                      'Техника и софт', 'Разное', 'Творчество',
                      'Игры', 'Японская культура']
        except Exception:
            return
        res = list(map(lambda x: data.json(), getboards))
        result = [x['id'] for i in boards for x in res[0][i]]
        return result

    def managethreads(self, board):
        inboard = 'https://2ch.hk/' + board + '/index.json'
        if board in self.boardlist():
            threads = requests.get(inboard).json()['threads']
            result = [i['thread_num'] for i in threads]
            return result

    def serfthread(self, board):
        try:
            threadnum = self.managethreads(board)
            inthread = 'https://2ch.hk/' + board + \
                       '/res/' + choice(threadnum) + '.json'
            getthread = requests.get(inthread).json()['threads'][0]['posts']
        except Exception:
            return
        return getthread

    def get2chpic(self, board):
        if self.managethreads(board) is None:
            return
        try:
            inthread = self.serfthread(board)
            result = [('https://2ch.hk/' +
                       board + '/' + i['files'][0]['path']) for i
                      in inthread if len(i['files']) != 0 and
                      i['files'][0]['type'] in [1, 2]]
        except Exception:
            return
        if result:
            return choice(result)
        else:
            return 'Ничего не найдено!'

    def _cmd_2ch(self, cirno, username, args):
        if not args or args in cirno.disallowed2ch:
            cirno.sendmsg(username + ': Доска отсутствует, либо запрещена.')
        else:
            randpic = self.get2chpic(args)
            if randpic:
                cirno.sendmsg(username + ': ' + randpic)


def setup():
    return Twochannel()
