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

userQuery = "select id, name, home from users "

# TODO DSN?

####
# Helper Functions
####

def userRow2json(row):
    return {"id" : row.id, "name" : row.name, "home" : row.home}




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

    # i() for insert
    def i(self, table, data):
        keys = data.keys()
        query = "insert into " + table + " (" + ", ".join(keys) + ") values (" \
              + ", ".join(["?"]*len(keys)) + ")"
        self.cursor.execute(query, *[data[k] for k in keys])
        self.connection.commit()

    def qUserWhere(self, col, val):
        # TODO clean this up. Do we even need this helper method?
        rows = self.q("select id, name, home from users where "+col+" = ?", val)
        if len(rows) == 0:
            return None
        return userQuery(rows[0])

    def getUserInfo(self, user):
        return self.qUserWhere("id", user)

    def getUserByEmail(self, email):
        return self.qUserWhere("email", email)

    # XXX this returns a list of user objects, not just IDs
    # Returns None on error TODO does that ever actually happen?
    def getUsersByNameRegex(self, regex):
        rows = self.q(userQuery + "where (name regexp ?)", regex, maxrows=100)
        return [userRow2json(r) for r in rows]

    def addNewUser(self, email, password, home, name):
        # XXX we're just putting these back into an object, after we already 
        # converted them to arguments. But perhaps that's not the end of the
        # world if it makes things make more sense. 
        self.i("users", {"email" : email,
                         "password" : password,
                         "home" : home,
                         "name" : name})
        return True # XXX When would we return false?

    def addTravelNotice(self, user, destination, start, end):
        # TODO Actually put the travel notice into the database
        return True

    def verifyPassword(self, user, password):
        rows = self.q("select password from users where id = ?", user)
        if len(rows) > 0 and rows[0].password == password:
            return True
        return False




# Exportable function to create DatabaseWrapper object. 
def dbwrapper():
    return DatabaseWrapper()
