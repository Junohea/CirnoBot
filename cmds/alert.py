from lib.utils import checkrank


class Alert(object):

    @checkrank(2)
    def _cmd_alert(self, cirno, username, args):
        afk = [i + ' ' for i in cirno.afklist if cirno.afklist[i]]
        result = ''.join(afk)
        if not afk:
            cirno.sendmsg('%s: Все на месте!' % username)
        elif args:
            cirno.sendmsg('%s %s ' % (args, result))
        else:
            cirno.sendmsg(result)


def setup():
    return Alert()
