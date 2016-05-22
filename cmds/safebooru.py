import requests
from random import choice


class Safebooru(object):

    def safebooru(self, query):
        try:
            data = requests.get(
                'http://safebooru.org/index.php?page=dapi&s=post&tags=' +
                query + '&q=index&json=1').json()
        except Exception:
            return 'Ничего не найдено!'
        result = ['http://safebooru.org/images/' + i['directory'] +
                  '/' + i['image'] for i in data]
        return choice(result)

    def _cmd_booru(self, cirno, username, args):
        result = self.safebooru(args)
        if result:
            cirno.sendmsg(username + ': ' + result)
        else:
            cirno.sendmsg(username + ': Ничего не найдено!')


def setup():
    return Safebooru()
