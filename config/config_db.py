from configparser import ConfigParser

URL_CONF = 'config/config_db.ini'
DSN = ''
USER = ''
PASSWORD = ''


def init_db():
    global DSN
    global USER
    global PASSWORD

    config = ConfigParser()
    config.read(URL_CONF)

    DSN = config['db']['DSN']
    USER = config['db']['USER']
    PASSWORD = config['db']['PASSWORD']


init_db()
