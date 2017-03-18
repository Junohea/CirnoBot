import requests
from lib.utils import throttle
from random import choice


class Dobrochan(object):

    def boards(self):
        try:
            result = requests.get('http://dobrochan.ru/index.json').json()['boards'].keys()
        except:
            return
        return result

    def get_threads_from_board(self, board):
        inboard = 'http://dobrochan.ru/%s/index.json' % board
        threads = requests.get(inboard).json()['boards'][board]['threads']
        result = [i['display_id'] for i in threads]
        return result

    def get_posts_form_thread(self, board, get_threads_from_board):
        try:
            req = 'http://dobrochan.ru/api/thread/last/%s/%s.json' \
                       % (board, choice(get_threads_from_board))
            posts = requests.get(req).json()['posts']

        except:
            return
        return posts

    def getdcpic(self, board):
        threads = self.get_threads_from_board(board)
        if threads is None:
            return
        try:
            inthread = self.get_posts_form_thread(board, threads)
            result = ['http://dobrochan.ru/%s' %
                      (i['files'][0]['src']) for
                      i in inthread if len(i['files']) != 0 and
                      i['files'][0]['type'] == "image" and i['files'][0]['rating'] == "sfw"]
        except:
            return
        return choice(result) if result else 'Ничего не найдено!'

    @throttle(8)
    def _cmd_dc(self, cirno, username, args):
        if args not in self.boards():
            cirno.sendmsg('%s: Доска не найдена.' % username)
        else:
            randpic = self.getdcpic(args)
            if randpic:
                cirno.sendmsg('%s: %s' % (username, randpic))


def setup():
    return Dobrochan()
