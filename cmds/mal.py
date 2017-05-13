from config import config
from lib.utils import throttle
import requests
from xml.etree import cElementTree as ET


class MyAnimeList(object):
    def getdict(self):
        username = config['API']['mal']
        response = requests.get('http://myanimelist.net/'
                                'malappinfo.php?status=all&u=%s' % username)

        result = {}
        for raw_entry in ET.fromstring(response.text):
            entry = {attr.tag: attr.text for attr in raw_entry}

            if 'series_title' in entry:
                entry_id = entry['series_title']

                result[entry_id] = {
                    'score': int(entry['my_score']),
                    'episode': int(entry['my_watched_episodes']),
                    'start': entry['my_start_date'],
                    'end': entry['my_finish_date']
                }

        return result

    @throttle(5)
    def _cmd_mal(self, cirno, username, args):
        data = self.getdict()
        if args in data.keys():
            title = data[args]
            score = title['score']
            episode = title['episode']
            start = title['start']
            end = title['end']
            if score == 0:
                score = 'Нет оценки'
            if (start, end) == ('0000-00-00', '0000-00-00'):
                start, end = 'Неизвестно', 'Неизвестно'
            result = '|%s| Оценка: %s, Просмотрено серий: %s,' \
                     ' Начали: %s, Закончили: %s' \
                     % (args, score, episode, start, end)
            cirno.sendmsg("%s: %s" % (username, result))
        else:
            cirno.sendmsg("%s: I didn't find this title in our MAL." % username)


def setup():
    return MyAnimeList()
