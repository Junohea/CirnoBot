from distutils.core import setup

setup(
    name='CirnoBot',
    version='1.0.1',
    packages=['lib', 'cmds'],
    url='http://tehtube.tv/',
    license='None',
    author='tehcpu',
    author_email='admin@tehtube.tv',
    description='', requires=['requests', 'gspread', 'oauth2client', 'bs4']
)
