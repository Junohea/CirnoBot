import requests
from lib.utils import throttle


class Quotes(object):

    def quotes(self):
        try:
            data = requests.get('http://api.forismatic.com/api/'
                                '1.0/?method=getQuote'
                                '&format=json&'
                                'lang=ru').json()['quoteText']
        except Exception:
            return
        return data

    @throttle(5)
    def _cmd_quote(self, cirno, username, args):
        result = self.quotes()
        cirno.sendmsg('%s: %s' % (username, result))


def setup():
    return Quotes()
