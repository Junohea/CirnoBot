import requests
from conf import config

KEY = config['API']['yandex']


class Translate(object):

    def translatedata(self, query):
        try:
            data = requests.get(
                'https://translate.yandex.net/api/v1.5/tr.json/translate?'
                'lang=ru&text=' + query + '&key=' + KEY).json()['text']
        except Exception:
            return
        return ''.join(data)

    def _cmd_translate(self, cirno, username, args):
        query = self.translatedata(args)
        cirno.sendmsg(username + ': ' + query)


def setup():
    return Translate()
