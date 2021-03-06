from lib.utils import checkrank


class Ratingpoll(object):

    @checkrank(2)
    def _cmd_poll(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Enter a title!' % username)
        else:
            options = {
                'opts': ['Did not watch?', '2', '3', '4', '5',
                         '6', '7', '8', '9', '10'],
                'title': 'Estimate? %s' % args,
                'timeout': 180,
                'obscured': True
            }
            cirno.openpoll(options)


def setup():
    return Ratingpoll()
