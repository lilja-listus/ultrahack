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


def verifyUserLogin(cookies):
    pass # TODO write this
    # TODO do redirect to login page if user is not logged in


def getUserFromCookie(cookies):
    verifyUserLogin(cookies)
    if "userID" in cookies:
        return cookies["userID"]
    else:
        return None # TODO this is an error



################################################################################
# Resource Classes                                                             #
################################################################################

# General class to handle DB wrapper
class GeneralResource(object):
    def __init__(self, dbwrapper):
        self.db = dbwrapper

class UsersResource(GeneralResource):
    def on_get(self, req, resp, user=None):
        if not user:
            user = getUserFromCookie(req.cookies)
        else:
            verifyUserLogin(cookies)

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
        data = json.load(req.stream)
        user = getUserFromCookie(req)
        start = data["start"] # TODO decode timestamp?
        end = data["end"] # TODO decode another timestamp?

        # TODO check for conflicts? Nope, better to do that in the front end
        # if we want to bother with it at all. 

        # Handle notifications of possible overlaping schedules in background
        if "audience" in data and type(data["audience"]) == list:
            background(handleOverlaps, (data["audience"],))
        else:
            pass # TODO some error. Perhaps just ignore?

        if self.db.addTravelNotice(user, data["destination"], start, end):
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_503 # XXX right error?





######
# Start everything up
#####

# Create a single database wrapper
dbwrapper = calldb.dbwrapper()

app = falcon.API()

app.add_route("/api/new_travel_notice", TravelNoticeResource(dbwrapper))
app.add_route("/api/user_info/{user}", UsersResource(dbwrapper))
