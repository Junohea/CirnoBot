from lib.utils import checkrank


class Alert(object):

    @checkrank(2)
    def _cmd_alert(self, cirno, username, args):
        afk = [i + ' ' for i in cirno.afklist if cirno.afklist[i]]
        result = ''.join(afk)
        if not afk:
            cirno.sendmsg(username + ': Все на месте!')
        elif args:
            cirno.sendmsg(args + ' ' + result)
        else:
            cirno.sendmsg(result)


def setup():
    return Alert()
