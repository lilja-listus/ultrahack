########
# These are the actual RESTful endpoints, implemented using Falcon.
#
# If we have time, we can try to re-write them using Amazon Lambda serverless
# functions, but for now let's stick to what we know works. 
#####

import falcon
import json



class UsersResource(object):
    # TODO do we need an init func? 

    def on_get(self, req, resp, user):
        # TODO call out to DB and get users






######
# Start everything up
#####

app = falcon.API()

app.add_route("/api/user_info/{user}", UsersResource())
