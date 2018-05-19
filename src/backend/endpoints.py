################################################################################
# These are the actual RESTful endpoints, implemented using Falcon.            #
#                                                                              #
# If we have time, we can try to re-write them using Amazon Lambda serverless  #
# functions, but for now let's stick to what we know works.                    #
################################################################################

import falcon
import json

from threading import Thread

# From local dir
import calldb


######
# Global Strings and other Magic Values
#####

userCookieName = "userID"
authTokenCookieName = "authToken"




#####
# Utility Functions
#####

def background(func, args):
    thread = Thread(target = func, args = args)
    thread.start()





################################################################################
# Resource-Related Helper Functions                                            #
################################################################################


# TODO a function to send emails and push notifs.
# I think there's an Amazon service for one of those at least?
# Think about Twilio for email sending? 


# Argument "audience" is a list of user IDs
def handleOverlaps(audience):
    for user in audience:
        pass # TODO

        # TODO get all of user's upcoming travel notices

        # TODO do the stuff described in design doc

def verifyLoginAndGetUser(cookies):
    # TODO verify that user is logged in
    # TODO throw an error to hijack request if not
    if "userID" in cookies:
        return cookies["userID"]
    else:
        return None # TODO this is an error, but it's probably our error.



################################################################################
# Resource Classes                                                             #
################################################################################

# General class to handle DB wrapper
class GeneralResource(object):
    def __init__(self, dbwrapper):
        self.db = dbwrapper


class LoginResource(GeneralResource):
    def on_post(self, req, resp):
        data = json.loads(str(req.stream.read()))

        user =self.db.getUserByEmail(data["email"]) if "email" in data else None
        if user and self.db.verifyPassword(user, data["password"]):
            resp.set_cookie(userCookieName, user, http_only=False)

            # TODO generate this in some actually useful manner
            authToken = "5678"

            resp.set_cookie(authTokenCookieName, authToken)

            resp.status = falcon.HTTP_200
            # XXX do we send back a specific redirect URL?
        else:
            resp.status = falcon.HTTP_401


class NewUserResource(GeneralResource):
    def on_post(self, req, resp):
        data = json.loads(str(req.stream.read()))

        if "email" in data and "password" in data and "home" in data:
            name = data["name"] if "name" in data else ""
            email = data["email"]
            password = data["password"]
            home = data["home"]
            if self.db.addNewUser(email, password, home, name):
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_503
        else:
            resp.status = falcon.HTTP_400 # Bad request


class SharingTargetsResource(GeneralResource):
    def on_get(self, req, resp, regex=""):
        # XXX so far, I don't think this will require authentication
        userInfoObjs = self.db.getUsersByNameRegex(regex)
        if userInfoObjs != None:
            # XXX add lists call when we actually have lists
            data = {"users" : userInfoObjs, "lists" : []}
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_503


class UsersResource(GeneralResource):
    def on_get(self, req, resp, user=None):
        loggedInUser = verifyLoginAndGetUser(req.cookies)
        if not user:
            user = loggedInUser

        userInfo = self.db.getUserInfo(user)

        if not userInfo:
            # XXX Is this enough?
            resp.status = falcon.HTTP_404 # User not found
        else:
            resp.status = falcon.HTTP_200
            # XXX I *think* this needs a string?
            resp.body = json.dumps(userInfo)


# XXX XXX XXX this class is basically untested at this point
class TravelNoticeResource(GeneralResource):
    def on_post(self, req, resp):
        user = verifyLoginAndGetUser(req.cookies)
        d = req.stream.read().decode("utf-8")
        print(d)
        data = json.loads(d)
        start = data["start"] # TODO decode timestamp?
        end = data["end"] # TODO decode another timestamp?

        # TODO TODO TODO For testing only!
        user = "1" if not user else user


        # TODO check that all fields are actually included in object

        # TODO check for conflicts? Nope, better to do that in the front end
        # if we want to bother with it at all. 

        planID = self.db.addTravelNotice(user, data["destination"], start, end)

        # Handle notifications of possible overlaping schedules in background
        if "audience" in data and type(data["audience"]) == list:
            background(handleOverlaps, (data["audience"],))
            # TODO update visibility table
        
        # TODO this whole check should be a try/catch
        if planID:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_503





######
# Start everything up
#####

# Create a single database wrapper
dbwrapper = calldb.dbwrapper()

app = falcon.API()

app.add_route("/api/login", LoginResource(dbwrapper))
app.add_route("/api/new_travel_notice", TravelNoticeResource(dbwrapper))
app.add_route("/api/new_user", NewUserResource(dbwrapper))
app.add_route("/api/sharing_targets/{regex}", SharingTargetsResource(dbwrapper))
app.add_route("/api/user_info/{user}", UsersResource(dbwrapper))
