import pyodbc
from dal.conn_credentials import SQL_DRIVER, SQL_SERVER, SQL_DB, SQL_UID, SQL_PWD, SQL_TRUSTED


class SqlServerAccess:

    def __init__(self):
        self.conn = None

    #def connect(self, driver, server, db, uid, pwd, trusted):
    def connect(self):
        if self.conn is None:
            conn_string = 'Driver=' + SQL_DRIVER + ';' +\
                          'Server=' + SQL_SERVER + ';' + \
                          'Database =' + SQL_DB + ';' + \
                          'UID=' + SQL_UID + ';' + \
                          'PWD=' + SQL_PWD + ';' + \
                          'Trusted_Connection=' + SQL_TRUSTED
            self.conn = pyodbc.connect(conn_string)
        return self.conn

    def close(self, driver, server, db, uid, pwd, trusted):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def reconnect(self, driver, server, db, uid, pwd, trusted):
        self.close()
        return self.connect()
