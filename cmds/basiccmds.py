from time import time
from datetime import timedelta
from random import choice, randint
from re import sub


class BasicCommands(object):

    def _cmd_uptime(self, cirno, username, args):
        uptime = time() - cirno.cirnostart
        uptime = "%s" % (timedelta(seconds=round(uptime)))
        cirno.sendmsg(username + ': В сети ' + uptime)

    def _cmd_pick(self, cirno, username, args):
        values = args.split(',')
        if len(values) > 1:
            cirno.sendmsg(username + ': ' + choice(values))
        else:
            cirno.sendmsg(username + ': Укажите не менее двух вариантов.')

    def _cmd_roll(self, cirno, username, args):
        randoften = randint(0, 10)
        if args and args.isdigit():
            setrand = randint(0, int(args))
            cirno.sendmsg(username + ': ' + "%s" % (setrand))
        else:
            cirno.sendmsg(username + ': ' + "%s" % (randoften))

    def _cmd_ask(self, cirno, username, args):
        if not args:
            cirno.sendmsg(username + ': Введите запрос!')
        else:
            answers = ['Определенно да', 'Да', 'Вероятно', 'Ни шанса',
                       'Определенно нет', 'Вероятность мала', 'Нет',
                       'Это не важно', 'Не стоит вскрывать эту тему',
                       'Не задавайте мне таких вопросов, мне нет 18']
            cirno.sendmsg(username + ': ' + choice(answers))

    def _cmd_who(self, cirno, username, args):
        if not args:
            cirno.sendmsg(username + ': Введите запрос!')
        else:
            query = sub(r'[^\w]', ' ', args)
            users = [key for key in cirno.userlist.keys()]
            cirno.sendmsg(choice(users) + " " + query)


def setup():
    return BasicCommands()
