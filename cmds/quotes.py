import requests


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

    def _cmd_quote(self, cirno, username, args):
        result = self.quotes()
        cirno.sendmsg(username + ': ' + result)


def setup():
    return Quotes()