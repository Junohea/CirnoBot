from lib.utils import checkrank
from lib.utils import writesettings, readsettings


class DenyUsers(object):

    @checkrank(2)
    def _cmd_deny(self, cirno, username, args):

        if args in cirno.userdict.keys() and cirno.userdict[args]['rank'] < 2:
            writesettings(args.split())
        else:
            cirno.sendmsg('%s: Нет такого пользователя, либо '
                          'его ранг равен модератору или выше.' % username)

    @checkrank(2)
    def _cmd_allow(self, cirno, username, args):
        denylist = readsettings()
        if args in denylist:
            writesettings(denylist.remove(args))
        else:
            cirno.sendmsg('%s: Не нашла такого пользователя'
                          ' в списке запрещенных!' % username)


def setup():
    return DenyUsers()
