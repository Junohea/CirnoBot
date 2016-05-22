import requests


class Rate(object):

    def ratedata(self):
        try:
            data = requests.post(
                'https://query.yahooapis.com/v1/public/yql?q=select+*+from+'
                'yahoo.finance.xchange+where+pair+=+%22USDRUB,EURRUB%22&'
                'format=json&env=store%3A%2F%2Fdatatables.org%'
                '2Falltableswithkeys'
                '&callback=').json()['query']['results']['rate']
        except Exception:
            return
        usd = data[0]['Name'] + ': ' + data[0]['Rate']
        eur = data[1]['Name'] + ': ' + data[1]['Rate']
        return usd, eur

    def _cmd_rate(self, cirno, username, args):
        data = self.ratedata()
        varsusd = ['usd', 'доллар', 'доллара']
        varseur = ['eur', 'евро']
        if data:
            usd = data[0]
            eur = data[1]
            if args.lower() in varsusd:
                cirno.sendmsg(username + ': ' + usd)
            elif args.lower() in varseur:
                cirno.sendmsg(username + ': ' + eur)
            else:
                cirno.sendmsg(username + ': Введите валюту (доступны usd и eur)!')


def setup():
    return Rate()
