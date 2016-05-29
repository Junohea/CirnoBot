from random import choice
from lib.utils import throttle


class Hit(object):

    @throttle(5)
    def _cmd_hit(self, cirno, username, args):
        user = args
        if user not in cirno.userdict.keys() \
                or user == cirno.name:
            cirno.sendmsg('%s: :miu:' % username)
        else:
            variants = ['/me пинает {}',
                        '/me отказывается пинать {} и дает ему печеньку.',
                        'Я боюсь пинать {}! Он же меня прибьет потом :cry:',
                        '/me замахнулась,'
                        ' но не справилась с управлением и упала',
                        '/me решает, что пинка недостаточно и избивает {}',
                        'Разве можно пинать такую няшу, как {}?'
                        ]
            result = choice(variants).format(user)
            cirno.sendmsg(result)


def setup():
    return Hit()
