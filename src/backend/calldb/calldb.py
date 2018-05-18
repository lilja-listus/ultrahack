#####
# Wrapper around database, allowing us to easily swap in and out different
# databases, even if they are radically different (i.e. SQL versus NoSQL).
#####




class DatabaseWrapper(object):
    def __init__(self):
        pass # TODO create DB as self.db

    def getUserInfo(self, userID):
        # TODO actually query some DB!
        return { 
                   "id" : userID,
                   "username" : "arya",
                   "name" : "A girl has no name",
                   "home" : {
                       "id" : "westeros_winterfell",
                       "name" : "Winterfell"
                   }
               }




# Exportable function to create DatabaseWrapper object. 
def dbwrapper():
    return DatabaseWrapper()
