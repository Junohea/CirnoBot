from random import choice
from lib.utils import throttle


class Hit(object):

    @throttle(5)
    def _cmd_hit(self, cirno, username, args):
        user = args
        if user not in cirno.userdict.keys() \
                or user == cirno.name:
            cirno.sendmsg('%s: The specified user was not found.' % username)
        else:
            variants = ['/me kicks {}',
                        '/me refuses to kick {} and gives him a cookie. /cookie',
                        "I'm afraid to kick {}! /o-o",
                        '/me swung(?),'
                        ' But failed to manage and fell(?)',
                        '/me Decides that a kick is not enough and gets ready to give {} a wood shampoo',
                        'Is it possible to kick a cunt like {}?'
                        ]
            result = choice(variants).format(user)
            cirno.sendmsg(result)


def setup():
    return Hit()
