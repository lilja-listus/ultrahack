########
# These are the actual RESTful endpoints, implemented using Falcon.
#
# If we have time, we can try to re-write them using Amazon Lambda serverless
# functions, but for now let's stick to what we know works. 
#####

import falcon
import json

# TODO if this doesn't work, we may need to 
import calldb



class UsersResource(object):
    def __init__(self, dbwrapper):
        self.dbwrapper = dbwrapper

    def on_get(self, req, resp, user):
        userInfo = self.dbwrapper.getUserInfo(user)

        if not userInfo:
            # XXX Is this enough?
            resp.status = falcon.HTTP_404 # User not found
        else:
            resp.status = falcon.HTTP_200
            # XXX I *think* this needs a string?
            resp.body = json.dumps(userInfo)







######
# Start everything up
#####

# Create a single database wrapper
dbwrapper = calldb.dbwrapper()

app = falcon.API()

app.add_route("/api/user_info/{user}", UsersResource(dbwrapper))
