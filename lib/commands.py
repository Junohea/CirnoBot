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


def altcommands():
    commandslist = loadplugins()
    ruscommandsdict = {
        "select": commandslist['commands'].get("pick", None),
        "roll": commandslist['commands'].get("roll", None),
        "8ball": commandslist['commands'].get("ask", None),
        "whois": commandslist['commands'].get("who", None),
        "online": commandslist['commands'].get("uptime", None),
        "quoth": commandslist['commands'].get("quote", None),
        "weather": commandslist['commands'].get("weather", None),
        "rate": commandslist['commands'].get("rate", None),
        "translate": commandslist['commands'].get("translate", None),
        "addit": commandslist['commands'].get("add", None),
        "spork": commandslist['commands'].get("random", None),
        "statistic": commandslist['commands'].get("stat", None),
        "hit": commandslist['commands'].get("hit", None),
        "query": commandslist['commands'].get("search", None),
        "q": commandslist['commands'].get("q", None),
        "picture": commandslist['commands'].get("pic", None),
        "gelbooru": commandslist['commands'].get("booru", None),
        "4ch": commandslist['commands'].get("4chan", None),
        "2chan": commandslist['commands'].get("2ch", None),
        "alert": commandslist['commands'].get("alert", None),
        "deny": commandslist['commands'].get("deny", None),
        "allow": commandslist['commands'].get("allow", None),
        "save": commandslist['commands'].get("save", None)
    }
    return ruscommandsdict


def handle(cirno, username, msg):
    commandslist = loadplugins()
    splice = msg.split(' ')
    command = splice.pop(0)[1:]
    args = ' '.join("%s" % x for x in splice).strip()
    if command in altcommands().keys():
        method = altcommands().get(command, None)
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
