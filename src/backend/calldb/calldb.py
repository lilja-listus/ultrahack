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
                   "username" : "arya",
                   "name" : "A girl has no name",
                   "home" : {
                       "id" : "westeros_winterfell",
                       "name" : "Winterfell"
                   }
               }

    def addTravelNotice(self, user, destination, start, end):
        # TODO Actually put the travel notice into the database
        return True




# Exportable function to create DatabaseWrapper object. 
def dbwrapper():
    return DatabaseWrapper()
