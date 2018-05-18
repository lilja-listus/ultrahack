#####
# Wrapper around database, allowing us to easily swap in and out different
# databases, even if they are radically different (i.e. SQL versus NoSQL).
#####




class DatabaseWrapper(object):
    def __init__(self):
        pass # TODO create DB as self.db

    def getUserInfo(self, user):
        # TODO actually query some DB!
        return { 
                   "id" : user,
                   "name" : "A girl has no name",
                   "home" : {
                       "id" : "westeros_winterfell",
                       "name" : "Winterfell"
                   }
               }

    def getUserByEmail(self, email):
        return "1234" # TODO get actual user ID, or None if no such user

    def addTravelNotice(self, user, destination, start, end):
        # TODO Actually put the travel notice into the database
        return True

    def verifyPassword(self, user, password):
        # TODO query DB for user's password and make sure it's correct.
        return True




# Exportable function to create DatabaseWrapper object. 
def dbwrapper():
    return DatabaseWrapper()
