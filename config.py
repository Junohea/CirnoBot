from configparser import ConfigParser

parser = ConfigParser()
parser.read('conf.cfg', encoding='utf-8')
config = dict()
for section in parser.sections():
    config[section] = dict(parser.items(section))
