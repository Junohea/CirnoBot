import re
import time


def checkrank(num):
    def getrank(func):
        def wrapper(self, cirno, username, args):
            rank = cirno.userdict[username]['rank']
            if rank >= num:
                return func(self, cirno, username, args)
        return wrapper
    return getrank


def throttle(num):
    def counter(func):
        def wrapper(self, cirno, username, args):
            last = time.time()
            if username not in cirno.cmdthrottle:
                cirno.cmdthrottle[username] = last
                return func(self, cirno, username, args)
            else:
                data = time.time() - cirno.cmdthrottle[username]
                cirno.cmdthrottle[username] = time.time()
                if data >= num:
                    return func(self, cirno, username, args)
                else:
                    return cirno.sendmsg('%s: Умерьте пыл.' % username)
        return wrapper
    return counter


def filterchat(msg):
    msg = re.sub("&#39;", "'", msg)
    msg = re.sub("&amp;", "&", msg)
    msg = re.sub("&lt;", "<", msg)
    msg = re.sub("&gt;", ">", msg)
    msg = re.sub("&quot;", "\"", msg)
    msg = re.sub("&#40;", "\(", msg)
    msg = re.sub("&#41;", "\)", msg)
    msg = re.sub("(<([^>]+)>)", "", msg)
    msg = re.sub("^[ \t]+", "", msg)
    return msg


def parsemedialink(url):
    if type(url) is not str:
        return {
            'id': None,
            'type': None
        }
    elif url.startswith('jw:'):
        return {
            'id': url[3:],
            'type': "jw"
        }
    elif url.startswith('rtmp://'):
        return {
            'id': url,
            'type': "rt"
        }
    elif 'youtube.com' in url:
        m = re.search(r'(https?://)?(www\.)?(youtube|youtu)'
                      r'\.(com|be)/(watch\?v=|v/)?([^&#]+)', url)
        return {
            'id': m.group(6),
            'type': 'yt'
        }

    elif 'google.com/file' in url:
        m = re.search(r'(docs.google.com|drive.google.com)'
                      '/(file/d)/([^/]*)', url)
        return {
            'id': m.group(3),
            'type': 'gd'
        }
    elif 'google.com/open' in url:
        m = re.search(r'(docs.google.com|drive.google.com)'
                      '/(.+?id=)?([^&#]+)', url)
        return {
            'id': m.group(3),
            'type': 'gd'
        }
    elif 'twitch.tv' in url:
        m = re.search(r'(https?://)?(twitch.tv)/([^&#]+)', url)
        return {
            'id': m.group(3),
            'type': 'tw'
        }
    elif 'livestream.com' in url:
        m = re.search(r'(https?://)?(livestream.com)/([^&#]+)', url)
        return {
            'id': m.group(3),
            'type': 'li'
        }
    elif 'ustream.tv' in url:
        m = re.search(r'(https?://)?(ustream.tv)/([^&#]+)', url)
        return {
            'id': m.group(3),
            'type': 'us'
        }
    elif 'vimeo.com' in url:
        m = re.search(r'(https?://)?(vimeo.com)/([^&#]+)', url)
        return {
            'id': m.group(3),
            'type': 'vi'
        }
    elif 'dailymotion.com' in url:
        m = re.search(r'(https?://)?(dailymotion.com/video)/([^&#]+)', url)
        return {
            'id': m.group(3),
            'type': 'dm'
        }
    elif 'soundcloud.com' in url:
        return {
            'id': url,
            'type': 'sc'
        }
    else:
        return {
            'id': None,
            'type': None
        }
