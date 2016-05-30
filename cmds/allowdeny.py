from lib.utils import checkrank


class DenyUsers(object):

    @checkrank(2)
    def _cmd_deny(self, cirno, username, args):
        blocklist = cirno.readsettings()
        if args not in blocklist['disallow']:
            if args in cirno.userdict.keys() and cirno.userdict[args]['rank'] < 2:
                cirno.settings['disallow'].append(args)
                cirno.writesettings()
            else:
                cirno.sendmsg('%s: Нет такого пользователя, либо '
                              'его ранг равен модератору или выше.' % username)
        else:
            cirno.sendmsg('%s: Пользователь уже заблокирован' % username)

    @checkrank(2)
    def _cmd_allow(self, cirno, username, args):
        blocklist = cirno.readsettings()
        if args in blocklist['disallow']:
            cirno.settings['disallow'].remove(args)
            cirno.writesettings()
        else:
            cirno.sendmsg('%s: Не нашла такого пользователя'
                          ' в списке запрещенных!' % username)


def setup():
    return DenyUsers()
