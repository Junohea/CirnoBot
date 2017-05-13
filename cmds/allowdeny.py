from lib.utils import checkrank, readsettings, writesettings


class DenyUsers(object):

    @checkrank(2)
    def _cmd_deny(self, cirno, username, args):
        blocklist = readsettings()
        if args not in blocklist['disallow']:
            if args in cirno.userdict.keys() \
                    and cirno.userdict[args]['rank'] < 2:
                cirno.settings['disallow'].append(args)
                writesettings(cirno)
            else:
                cirno.sendmsg('%s: There is no such user, or '
                              'their rank is equal to moderator or higher.' % username)
        else:
            cirno.sendmsg('%s: The user is already blocked' % username)

    @checkrank(2)
    def _cmd_allow(self, cirno, username, args):
        if args in readsettings()['disallow']:
            cirno.settings['disallow'].remove(args)
            writesettings(cirno)
        else:
            cirno.sendmsg('%s: User not found in'
                          ' the list of banned users.' % username)


def setup():
    return DenyUsers()
