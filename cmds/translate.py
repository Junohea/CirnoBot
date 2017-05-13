import requests
from config import config
from lib.utils import throttle

KEY = config['API']['yandex']


class Translate(object):

    def translatedata(self, query):
        try:
            data = requests.get(
                'https://translate.yandex.net/api/v1.5/tr.json/translate?'
                'lang=en&text=%s&key=%s' % (query, KEY)).json()['text']
        except Exception:
            return
        return ''.join(data)

    @throttle(5)
    def _cmd_translate(self, cirno, username, args):
        query = self.translatedata(args)
        cirno.sendmsg('%s: %s' % (username, query))


def setup():
    return Translate()
