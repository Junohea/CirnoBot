import requests
from lib.utils import throttle
from random import choice


class Safebooru(object):

    def safebooru(self, query):
        try:
            data = requests.get(
                'http://safebooru.org/index.php?page=dapi'
                '&s=post&tags=%s&q=index&json=1' % query).json()
        except Exception:
            return
        result = ['http://safebooru.org/images/%s/%s'
                  % (i['directory'], i['image']) for i in data]
        return choice(result)

    @throttle(5)
    def _cmd_booru(self, cirno, username, args):
        result = self.safebooru(args)
        if result:
            cirno.sendmsg('%s: %s' % (username, result))
        else:
            cirno.sendmsg('%s: Nothing found!' % username)


def setup():
    return Safebooru()
