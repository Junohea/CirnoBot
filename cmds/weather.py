import requests
from conf import config
from lib.utils import throttle

KEY = config['API']['weather']


class Weather(object):

    def weatherdata(self, city):
        url = 'http://api.openweathermap.org/data/2.5/weather?' \
              'q=%s&lang=ru&units=metric&APPID=%s' % (city, KEY)
        if city.isalpha():
            try:
                data = requests.get(url).json()
                desc = data['weather'][0]['description'].capitalize()
                temp = '%s' % round(data['main']['temp'])
                result = 'Погода в городе %s: %s %s°C' \
                         % (city.capitalize(), desc, temp)
            except Exception:
                return
            return result
        else:
            return 'Неверно указан город'

    def forecast(self, city):
        url = 'http://api.openweathermap.org/data/2.5/forecast/daily?' \
              'q=%s&mode=json&lang=ru&' \
              'units=metric&cnt=3&APPID=%s' % (city, KEY)
        if city.isalpha():
            try:
                data = requests.get(url).json()['list']
                temp = [i['temp']['day'] for i in data]
                desc = [x['weather'][0]['description'] for x in data]
                tomorrow = '%s %s' % (desc[1].capitalize(), round(temp[1]))
                aftertmrw = '%s %s' % (desc[2].capitalize(), round(temp[2]))
            except Exception:
                return
            return tomorrow, aftertmrw
        else:
            return 'Неверно указан город'

    @throttle(5)
    def _cmd_weather(self, cirno, username, args):
        data = args.split()
        if not args:
            cirno.sendmsg('%s: Укажите город!' % username)
            return
        city = data[0]
        forecast = self.forecast(city)
        today = self.weatherdata(city)
        tomorrow = 'Погода в городе %s на завтра: %s°C' \
                   % (city.capitalize(), forecast[0])
        aftertomorrow = 'Погода в городе %s на послезавтра: ' \
                        '%s°C' % (city.capitalize(), forecast[1])

        if today and len(data) < 2:
            cirno.sendmsg('%s: %s' % (username, today))
        elif forecast and data[1] == 'завтра':
            cirno.sendmsg('%s: %s' % (username, tomorrow))
        elif forecast and data[1] == 'послезавтра':
            cirno.sendmsg('%s: %s' % (username, aftertomorrow))


def setup():
    return Weather()
