from time import time
from datetime import timedelta
from random import choice, randint


class BasicCommands(object):

    def _cmd_uptime(self, cirno, username, args):
        uptime = time() - cirno.cirnostart
        uptime = '%s' % (timedelta(seconds=round(uptime)))
        cirno.sendmsg('%s: В сети: %s' % (username, uptime))

    def _cmd_pick(self, cirno, username, args):
        values = args.split(',')
        if len(values) > 1:
            cirno.sendmsg('%s: %s' % (username, choice(values)))
        else:
            cirno.sendmsg('%s: Укажите не менее двух вариантов.' % username)

    def _cmd_roll(self, cirno, username, args):
        randoften = randint(0, 10)
        if args and args.isdigit():
            setrand = randint(0, int(args))
            cirno.sendmsg('%s: %s' % (username, setrand))
        else:
            cirno.sendmsg('%s: %s' % (username, randoften))

    def _cmd_ask(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Введите запрос!' % username)
        else:
            answers = ['Определенно да', 'Да', 'Вероятно', 'Ни шанса',
                       'Определенно нет', 'Вероятность мала', 'Нет',
                       'Это не важно', 'Не стоит вскрывать эту тему']
            cirno.sendmsg('%s: %s' % (username, choice(answers)))

    def _cmd_who(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Введите запрос!' % username)
        else:
            users = list(cirno.userdict.keys())
            args = args.replace('?', '') if args.endswith('?') else args
            cirno.sendmsg('%s %s' % (choice(users), args))


def setup():
    return BasicCommands()
