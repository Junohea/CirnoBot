import sqlite3


class CirnoDatabase(object):
    def __init__(self):
        self.conn = sqlite3.connect('cirnodb.db', timeout=60)
        self.c = self.conn.cursor()
        self.createtables()

    def createtables(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS users(uname TEXT,"
                       " PRIMARY KEY(uname))")
        self.c.execute("CREATE TABLE IF NOT EXISTS chat(timestamp INTEGER,"
                       " username TEXT, msg TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS pics(pictures TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS quotes(chatquote TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS version(key TEXT, "
                       "value TEXT, PRIMARY KEY(key))")
        self.updatetables()

    def updatetables(self):
        if self.getversion() is None:
            self.c.execute("INSERT INTO version(key, value) VALUES (?, ?)",
                           ['dbversion', '1'])
            self.c.execute("ALTER TABLE users ADD rank INTEGER")
            self.conn.commit()

    def getversion(self):
        self.c.execute("SELECT value FROM version WHERE key = 'dbversion'")
        r = self.c.fetchone()
        if r:
            return r[0]
        else:
            return None

    def insertchat(self, timestamp, username, msg):
        self.c.execute("INSERT INTO chat VALUES(?, ?, ?)",
                       (timestamp, username, msg))
        self.conn.commit()

    def insertuser(self, username, rank):
        if username is None:
            return

        self.c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)",
                       (username, rank))
        self.conn.commit()

    def insertuserrank(self, username, rank):
        self.c.execute("UPDATE users SET rank = ? WHERE uname = ?",
                       (rank, username))
        self.conn.commit()

    def getuserrank(self, username):
        self.c.execute("SELECT rank FROM users WHERE uname= ?", [username])
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None

    def getrandom(self, username):
        username = username.split(' ')[0]

        if username:
            self.c.execute("SELECT timestamp, username, msg FROM chat "
                           "WHERE username = ? COLLATE NOCASE "
                           "ORDER BY RANDOM() LIMIT 1", [username])
            r = self.c.fetchone()
            if r:
                return list(r)
            else:
                return None
        else:
            self.c.execute("SELECT timestamp, username, msg FROM "
                           "chat WHERE msg NOT LIKE '/me%' AND "
                           "msg NOT LIKE '$%' ORDER BY RANDOM() LIMIT 1")
            r = self.c.fetchone()
            if r:
                return list(r)
            else:
                return None

    def getquantity(self, username):
        username = username.split(' ')[0]
        self.c.execute("SELECT COUNT(*) AS quantity FROM chat"
                       " WHERE username = ? COLLATE NOCASE LIMIT 1",
                       [username])
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None

    def emotesquantity(self, username):
        username = username.split(' ')[0]
        self.c.execute("SELECT COUNT(*) AS quantity, msg FROM chat"
                       " WHERE username = ? AND (msg LIKE ':%:' OR msg LIKE '%:  :%:') COLLATE NOCASE LIMIT 1",
                       [username])
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None

    def getpic(self):
        self.c.execute("SELECT pictures FROM pics ORDER BY"
                       " RANDOM() LIMIT 1")
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None

    def getquote(self):
        self.c.execute("SELECT chatquote FROM quotes ORDER BY"
                       " RANDOM() LIMIT 1")
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None
