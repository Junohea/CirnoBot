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

    def forecast(self, city):
        url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' \
              + city + "&mode=json&lang=ru&units=metric&cnt=3&APPID=" + KEY
        if city.isalpha():
            try:
                data = requests.get(url).json()['list']
                temp = [i['temp']['day'] for i in data]
                desc = [x['weather'][0]['description'] for x in data]
                tomorrow = desc[1].capitalize() + ' ' + str(round(temp[1]))
                aftertmrw = desc[2].capitalize() + ' ' + str(round(temp[2]))
            except Exception:
                return
            return tomorrow, aftertmrw
        else:
            return 'Неверно указан город'

    def _cmd_weather(self, cirno, username, args):
        data = args.split()
        if not args:
            cirno.sendmsg(username + ': Укажите город!')
            return
        city = data[0]
        forecast = self.forecast(city)
        today = self.weatherdata(city)
        tomorrow = 'Погода в городе ' + city + \
                   ' на завтра: ' + forecast[0] + '°C'
        aftertomorrow = 'Погода в городе ' + city + \
                        ' на послезавтра: ' + forecast[1] + '°C'

        if today and len(data) < 2:
            cirno.sendmsg(username + ': ' + today)
        elif forecast and data[1] == 'завтра':
            cirno.sendmsg(username + ': ' + tomorrow)
        elif forecast and data[1] == 'послезавтра':
            cirno.sendmsg(username + ': ' + aftertomorrow)


def setup():
    return Weather()
