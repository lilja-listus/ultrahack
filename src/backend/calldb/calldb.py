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

def travelNoticeRow2json(row):
    return {"id" : row.id,
            "destination" : row.destination,
            "start" : row.start_time,
            "end" : row.end_time}



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
    def q(self, *query):
        self.cursor.execute(*query)
        return self.cursor.fetchone()

    # i() for insert
    def i(self, table, data):
        keys = data.keys()
        query = "insert into " + table + " (" + ", ".join(keys) + ") values (" \
              + ", ".join(["?"]*len(keys)) + ")"
        self.cursor.execute(query, *[data[k] for k in keys])
        rowID = self.cursor.execute("select last_insert_id()").fetchone()
        self.connection.commit()
        return rowID[0]

    def qUserWhere(self, col, val):
        # TODO clean this up. Do we even need this helper method?
        row = self.q("select id, name, home from users where "+col+" = ?", val)
        if row == None:
            return None
        return userRow2json(row)

    def getListsByNameRegex(self, owner, regex):
        regex = regex if regex else "" # Regex may not be None
        sql = '''select 
                     user_lists.id, 
                     user_lists.name, 
                     user_list_members.user,
                     users.name,
                     users.home 
                 from user_lists join user_list_members 
                            on user_lists.id = user_list_members.user_list
                                 join users 
                            on user_list_members.user = users.id 
                 where (user_lists.owner = ?) and (user_lists.name regexp ?)'''
        self.cursor.execute(sql, owner, regex)
        rows = self.cursor.fetchall() # XXX A bit dangerous. Cap list size?
        data = {}
        for row in rows:
            if row[0] in data:
                data[row[0]]["members"].append({"id" : row[2],
                                                "name" : row[3],
                                                "home" : row[4]})
            else:
                data[row[0]] = {"id" : row[0],
                                "name" : row[1],
                                "members" : [{"id" : row[2],
                                              "name" : row[3],
                                              "home" : row[4]}]}
        return [data[k] for k in data]

    # XXX Takes a list of list IDs, or a single list ID (string).
    def getListMembers(self, owner, user_lists):
        if type(user_lists) != list:
            user_lists = [user_lists]
        if len(user_lists) <= 0:
            return []
        sql = '''select user_list_members.user 
                 from user_lists join user_list_members 
                            on user_lists.id = user_list_members.user_list 
                 where (user_lists.owner = ?) 
                    and user_list_members.user_list in '''
        sql += "(" + ", ".join(["?"] * len(user_lists)) + ")"
        self.cursor.execute(sql, owner, *[i for i in user_lists])
        rows = self.cursor.fetchall()
        return [r[0] for r in rows]

    def getTravelNotice(self, planID):
        sql = '''select id, destination, start_time, end_time from travel_plans
                 where id = ?'''
        return travelNoticeRow2json(self.q(sql, planID))

    def getTravelNoticeOverlaps(self, user, destination, start, end):
        sql = '''select id, destination, start_time, end_time from travel_plans
                 where (user = ?) and (destination = ?)
                    and (start_time < ?) and (end_time > ?)'''
        self.cursor.execute(sql, user, destination, start, end)
        return [travelNoticeRow2json(r) for r in self.cursor.fetchall()]

    def getUserInfo(self, user):
        return self.qUserWhere("id", user)

    def getUserByEmail(self, email):
        return self.qUserWhere("email", email)

    # XXX this returns a list of user objects, not just IDs
    # Returns None on error TODO does that ever actually happen?
    def getUsersByNameRegex(self, regex):
        regex = regex if regex else "" # Regex may not be None
        self.cursor.execute(userQuery + "where (name regexp ?)", regex)
        rows = self.cursor.fetchmany(100)
        return [userRow2json(r) for r in rows]

    def getVisibilityByTravelNotice(self, planID):
        sql = "select user from visibility where travel_plan = ?"
        self.cursor.execute(sql, planID)
        return [r[0] for r in self.cursor.fetchall()]

    def addNewUser(self, email, password, home, name):
        # XXX we're just putting these back into an object, after we already 
        # converted them to arguments. But perhaps that's not the end of the
        # world if it makes things make more sense. 
        return self.i("users", {"email" : email,
                                "password" : password,
                                "home" : home,
                                "name" : name})

    def addUserList(self, owner, name):
        return self.i("user_lists", {"owner" : owner, "name" : name})

    def addUserListMembers(self, user_list, members):
        # TODO this pattern is ripe for factoring out
        if not members:
            return
        query = "insert into user_list_members (user_list, user) values " \
              + ", ".join(["(?, ?)"] * len(members)) + ";"
        args = []
        for member in members:
            args.append(user_list)
            args.append(member)
        self.cursor.execute(query, *args)
        self.connection.commit()

    # TODO check: can that query fail?
    def addTravelNotice(self, user, destination, start, end):
        return self.i("travel_plans", {"user" : user,
                                       "destination" : destination,
                                       "start_time" : start,
                                       "end_time" : end})

    def addVisibilityRow(self, travel_plan, audience):
        if not audience:
            return
        query = "insert into visibility (travel_plan, user) values " \
              + ", ".join(["(?, ?)"] * len(audience)) + ";"
        args = []
        for user in audience:
            args.append(travel_plan)
            args.append(user)
        self.cursor.execute(query, *args)
        self.connection.commit()

    def verifyPassword(self, user, password):
        rows = self.q("select password from users where id = ?", user)
        if len(rows) > 0 and rows[0].password == password:
            return True
        return False




# Exportable function to create DatabaseWrapper object. 
def dbwrapper():
    return DatabaseWrapper()
