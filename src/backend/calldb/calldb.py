#####
# Wrapper around database, allowing us to easily swap in and out different
# databases, even if they are radically different (i.e. SQL versus NoSQL).
#####

import pyodbc


###
# Magic Values
###

dburl = "vastomadb.c9xefv9wj6wi.eu-central-1.rds.amazonaws.com"
dbpw = "vastomapassword" # TODO get this out of the repo
dbname = "vastomadb"

# TODO DSN?

class DatabaseWrapper(object):
    def __init__(self):
        # TODO this is ugly, but we only really need it here for testing
        self.connection = pyodbc.connect("DRIVER={MySQL ODBC 8.0 Driver};SERVER=vastomadb.c9xefv9wj6wi.eu-central-1.rds.amazonaws.com;UID=vastomadbuser;PWD=vastomapassword")

        # XXX pyodbc documentation implies that this will work
        self.connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        self.connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        self.connection.setencoding(encoding='utf-8')

        self.cursor = self.connection.cursor()
        self.cursor.execute("use " + dbname + ";")

    # Just a shorter name for convenience
    def q(self, *query, maxrows=1):
        self.cursor.execute(*query)
        return self.cursor.fetchmany(maxrows)

    def qUserWhere(self, col, val):
        rows = self.q("select id, name, home from users where "+col+" = ?", val)
        if len(rows) == 0:
            return None
        return {"id" : rows[0].id, "name" : rows[0].name, "home" : rows[0].home}

    def getUserInfo(self, user):
        return self.qUserWhere("id", user)

    def getUserByEmail(self, email):
        return self.qUserWhere("email", email)

    # XXX this returns a list of user objects, not just IDs
    # Returns None on error
    def getUsersByNameRegex(self, regex):
        return [] # TODO Get all users whose names match given regex

    def addNewUser(self, email, password, home, name):
         return True # TODO

    def addTravelNotice(self, user, destination, start, end):
        # TODO Actually put the travel notice into the database
        return True

    def verifyPassword(self, user, password):
        # TODO query DB for user's password and make sure it's correct.
        return True




# Exportable function to create DatabaseWrapper object. 
def dbwrapper():
    return DatabaseWrapper()
