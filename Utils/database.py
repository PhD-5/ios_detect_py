import data
import sqlite3
class DBServer():
    def setup(self):
        try:
            con = sqlite3.connect("ios.db")
            c = con.cursor()
            c.execute('''create table metadata (
                      uuid text primary key,
                      name text,
                      app_version text,
                      bundle_id text,
                      bundle_directory text,
                      data_directory text,
                      binary_directory text,
                      binary_path text,
                      binary_name text,
                      entitlements text,
                      platform_version text,
                      sdk_version text,
                      minimum_os text,
                      url_handlers text,
                      architectures text
                      )''')

            c.execute('''create table strings (
            uuid text,
            str text unique
            )''')

            con.commit()
            con.close()
        except sqlite3.Error as e:
            print e

    def on(self):
        try:
            data.db = self
            self.con = sqlite3.connect("ios.db")
            self.c = self.con.cursor()
            data.c = self.c
        except sqlite3.Error as e:
            print e.args[0]

    def down(self):
        try:
            self.con.commit()
            self.con.close()
            print "DBServer Down"
        except sqlite3.Error as e:
            print e.args[0]

    def execute(self, query):
        try:
            self.c.execute(query)
            return self.c.fetchall()
        except sqlite3.Error as e:
            print e.args[0]
            return False

    def execute(self, query, args):
        try:
            self.c.execute(query, args)
            return self.c.fetchall()
        except sqlite3.Error as e:
            print "here", e.args[0]
            return False




