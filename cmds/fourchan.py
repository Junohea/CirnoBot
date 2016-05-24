import requests
from random import choice, randint


class Fourchan(object):

    def fourchanboards(self):
        boardlist = 'https://a.4cdn.org/boards.json'
        try:
            boards = requests.get(boardlist).json()['boards']
            resboards = [board['board'] for board in boards]
        except Exception:
            return
        return resboards

    def get4chanthreads(self, board):
        threadlist = 'https://a.4cdn.org/' + board + '/threads.json'
        resboards = self.fourchanboards()
        if board in resboards and resboards:
            threads = requests.get(threadlist).json()
            req = [x['threads'] for x in threads]
            result = [x['no'] for x in sum(req, []) if x]
            return result

    def get4chanpics(self, board):
        threads = self.get4chanthreads(board)
        inthread = "https://a.4cdn.org/" + board + "/thread/{0}.json"
        main = 'https://i.4cdn.org/' + board + "/"
        if threads is None:
            return
        posts = requests.get(inthread.format(choice(threads))).json()["posts"]
        allowext = {'.jpg', '.png', '.gif'}
        result = ["%s%s%s" % (main, post['tim'], post['ext']) for post in posts
                  if ('filename' in post) and
                  (post.get('ext', None) in allowext)]
        if result:
            return choice(result)
        else:
            return 'Ничего не найдено!'

    def _cmd_4chan(self, cirno, username, args):
        if not args or args in cirno.disallowed4ch:
            cirno.sendmsg(username + ': Доска отсутствует, либо запрещена.')
        else:
            randpic = self.get4chanpics(args)
            if randpic:
                cirno.sendmsg(username + ': ' + randpic)


def setup():
    return Fourchan()
