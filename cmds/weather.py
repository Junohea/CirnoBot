import requests
from conf import config

KEY = config['API']['weather']


class Weather(object):

    def weatherdata(self, city):
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' \
              + city + "&lang=ru&units=metric&APPID=" + KEY
        if city.isalpha():
            try:
                data = requests.get(url).json()
                desc = data['weather'][0]['description'].capitalize()
                temp = "%s" % (round(data['main']['temp']))
                result = 'Погода в городе ' + city.capitalize() \
                         + ": " + desc + ' ' + temp + '°C'
            except Exception:
                return
            return result
        else:
            return 'Неверно указан город'

    def _cmd_weather(self, cirno, username, args):
        result = self.weatherdata(args)
        if not args:
            cirno.sendmsg(username + ': Укажите город!')
            return

        if result:
            cirno.sendmsg(username + ': ' + result)


def setup():
    return Weather()
