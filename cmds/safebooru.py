import requests
from random import choice


class Safebooru(object):

    def safebooru(self, query):
        try:
            data = requests.get(
                'http://safebooru.org/index.php?page=dapi'
                '&s=post&tags=%s&q=index&json=1' % query).json()
        except Exception:
            return 'Ничего не найдено!'
        result = ['http://safebooru.org/images/%s/%s'
                  % (i['directory'], i['image']) for i in data]
        return choice(result)

    def _cmd_booru(self, cirno, username, args):
        result = self.safebooru(args)
        if result:
            cirno.sendmsg('%s: %s' % (username, result))
        else:
            cirno.sendmsg('%s: Ничего не найдено!' % username)


def setup():
    return Safebooru()
