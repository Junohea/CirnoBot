from lib.utils import checkrank


class Alert(object):
    @checkrank(2)
    def _cmd_alert(self, cirno, username, args):
        data = [(k, v['afk']) for k, v
                in cirno.userdict.items() if v['afk']]
        afklist = [i[0] for i in data]
        result = ' '.join(afklist)
        if not afklist:
            cirno.sendmsg('%s: Everything is in place(?)!' % username)
        elif args:
            cirno.sendmsg('%s %s ' % (args, result))
        else:
            cirno.sendmsg(result)


def setup():
    return Alert()
