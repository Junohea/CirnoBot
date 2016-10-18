import importlib
import os


def importplugins(path):
    files = os.listdir(path)
    importpath = path.replace('/', '.')
    modulenames = [importpath + i[:-3] for i in files
                   if not i.startswith('_') and i.endswith('.py')]
    modules = list(map(importlib.import_module, modulenames))
    return modules


def loadplugins():
    modules = importplugins('cmds/')
    triggers = {'commands': {}}
    for module in modules:
        instance = module.setup()
        for method in dir(instance):
            if method.startswith('_cmd_'):
                trigger = '%s' % method[5:]
                triggers['commands'][trigger] \
                    = getattr(instance, method)
    return triggers


def ruscommands():
    commandslist = loadplugins()
    ruscommandsdict = {
        "выбор": commandslist['commands'].get("pick", None),
        "ролл": commandslist['commands'].get("roll", None),
        "спросить": commandslist['commands'].get("ask", None),
        "кто": commandslist['commands'].get("who", None),
        "аптайм": commandslist['commands'].get("uptime", None),
        "цитата": commandslist['commands'].get("quote", None),
        "погода": commandslist['commands'].get("weather", None),
        "курс": commandslist['commands'].get("rate", None),
        "переведи": commandslist['commands'].get("translate", None),
        "добавь": commandslist['commands'].get("add", None),
        "рандом": commandslist['commands'].get("random", None),
        "статистика": commandslist['commands'].get("stat", None),
        "пни": commandslist['commands'].get("hit", None),
        "загугли": commandslist['commands'].get("search", None),
        "q": commandslist['commands'].get("q", None),
        "пик": commandslist['commands'].get("pic", None),
        "booru": commandslist['commands'].get("booru", None),
        "4chan": commandslist['commands'].get("4chan", None),
        "2ch": commandslist['commands'].get("2ch", None),
        "алерт": commandslist['commands'].get("alert", None),
        "запрети": commandslist['commands'].get("deny", None),
        "разреши": commandslist['commands'].get("allow", None),
        "сохрани": commandslist['commands'].get("save", None)
    }
    return ruscommandsdict


def handle(cirno, username, msg):
    commandslist = loadplugins()
    splice = msg.split(' ')
    command = splice.pop(0)[1:]
    args = ' '.join("%s" % x for x in splice).strip()
    if command in ruscommands().keys():
        method = ruscommands().get(command, None)
    else:
        method = commandslist['commands'].get(command, None)
    if method:
        try:
            return method(cirno, username, args)
        except:
            if cirno.what:
                cirno.sendmsg("%s: %s" % (username, cirno.what))
            else:
                return
    else:
        return
