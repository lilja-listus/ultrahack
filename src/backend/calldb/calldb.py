#####
# Wrapper around database, allowing us to easily swap in and out different
# databases, even if they are radically different (i.e. SQL versus NoSQL).
#####




class DatabaseWrapper(object):
    def __init__(self):
        pass # TODO create DB as self.db

    def getUserInfo(self, uesrID):
        return {} # TODO return something for real




# Exportable function to create DatabaseWRapper object. 
