from time import time
from datetime import timedelta
from random import choice, randint
from lib.utils import checkrank, throttle


class BasicCommands(object):
    @throttle(5)
    def _cmd_uptime(self, cirno, username, args):
        if len(args) > 0 and args in cirno.userdict.keys():
            return self.uptime_by_username(cirno, username, args)
        try:
            cirno.userdict[username]['uptime']
        except KeyError:
            return cirno.sendmsg('%s: Failed to get network time(?).' % username)
        uptime = time() - cirno.userdict[username]['uptime']
        uptime = '%s' % (timedelta(seconds=round(uptime)))
        locale = uptime.replace('days', 'дней') if 'days' in uptime else uptime.replace('day', 'день')
        cirno.sendmsg('%s: Your time: %s' % (username, locale))

    def uptime_by_username(self, cirno, username, args):
        uptime = time() - cirno.userdict[args]['uptime']
        uptime = '%s' % (timedelta(seconds=round(uptime)))
        locale = uptime.replace('days', 'дней') if 'days' in uptime else uptime.replace('day', 'день')
        cirno.sendmsg('%s: %s Is online: %s' % (username, args, locale))

    def _cmd_pick(self, cirno, username, args):
        values = args.split(',')
        if len(values) > 1:
            cirno.sendmsg('%s: %s' % (username, choice(values)))
        else:
            cirno.sendmsg('%s: Please specify at least two options.' % username)

    def _cmd_roll(self, cirno, username, args):
        randoften = randint(0, 10)
        if args and args.isdigit():
            setrand = randint(0, int(args))
            cirno.sendmsg('%s: %s' % (username, setrand))
        else:
            cirno.sendmsg('%s: %s' % (username, randoften))

    def _cmd_ask(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Ask your question!' % username)
        else:
            answers = ['Definitely yes', 'Yes', 'Probably', 'No chance',
                       'Definitely not', 'The probability is small', 'No',
                       "It doesn't matter", 'Do not open this topic(?)']
            cirno.sendmsg('%s: %s' % (username, choice(answers)))

    def _cmd_who(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Enter the query!' % username)
        else:
            users = list(cirno.userdict.keys())
            args = args.replace('?', '') if args.endswith('?') else args
            cirno.sendmsg('%s %s' % (choice(users), args))

    @checkrank(2)
    def _cmd_voteskip(self, cirno, username, args):
        cirno.handle_voteskip()


def setup():
    return BasicCommands()
