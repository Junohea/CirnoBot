import bs4
import requests
from lib.utils import throttle


class GoogleSearch(object):

    def search(self, query):
        headers = {'user-agent': 'Mozilla/5.0'
                   '(Windows NT 6.1; WOW64; rv:46.0)'}
        req = requests.get('https://www.google.com/search?q=%s'
                           % query, headers=headers)
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        site = [cite.text for cite in soup.findAll('cite')]
        desc = [li.text for li in soup.findAll('span', attrs={'class': 'st'})]
        result = '%s %s' % (site[0], desc[0])
        return result

    @throttle(5)
    def _cmd_search(self, cirno, username, query):
        if len(query) == 0:
            cirno.sendmsg('%s: Enter a query!' % username)
            return
        data = self.search(query)
        if data:
            cirno.sendmsg('%s: %s' % (username, data))


def setup():
    return GoogleSearch()
