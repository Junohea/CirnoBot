from distutils.core import setup

setup(
    name='CirnoBot',
    version='1.1.0',
    packages=['lib', 'cmds'],
    url='http://tehtube.tv/',
    license='None',
    author='tehcpu',
    author_email='admin@tehtube.tv',
    description='', requires=['socketIO_client', 'requests',
                              'gspread', 'oauth2client', 'bs4']
)
