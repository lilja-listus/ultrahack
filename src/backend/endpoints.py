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
import notify


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

def getReqJsonBody(req):
    return json.loads(req.stream.read().decode("utf-8"))



################################################################################
# Resource-Related Helper Functions                                            #
################################################################################


# TODO a function to send emails and push notifs.
# I think there's an Amazon service for one of those at least?
# Think about Twilio for email sending? 





def verifyLoginAndGetUser(cookies):
    # TODO verify that user is logged in
    # TODO throw an error to hijack request if not
    if userCookieName in cookies:
        return cookies[userCookieName]
    else:
        return "1" # TODO this is an error, but it's probably our error.
                   # Returning junk data for now so tests don't fail. 



################################################################################
# Resource Classes                                                             #
################################################################################

# General class to handle DB wrapper
class GeneralResource(object):
    def __init__(self, dbwrapper):
        self.db = dbwrapper

    # This is here because it requires the database. 
    def convertAudience(self, owner, audience):
        listIDs = [a.strip("#") for a in audience if a.startswith("#")]
        userIDs = set([a for a in audience if not a.startswith("#")])
        userIDs.update(self.db.getListMembers(owner, listIDs))
        return userIDs


class LoginResource(GeneralResource):
    def on_post(self, req, resp):
        d = req.stream.read().decode("utf-8")
        print(d)
        data = json.loads(d)

        user =self.db.getUserByEmail(data["email"]) if "email" in data else None
        if user and self.db.verifyPassword(user, data["password"]):
            resp.set_cookie(userCookieName, user, http_only=False)

            # TODO generate this in some actually useful manner
            authToken = "5678"

            resp.set_cookie(authTokenCookieName, authToken)

            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class NewUserResource(GeneralResource):
    def on_post(self, req, resp):
        d = req.stream.read().decode("utf-8")
        print(d)
        data = json.loads(d)

        if "email" in data and "password" in data and "home" in data:
            name = data["name"] if "name" in data else ""
            email = data["email"]
            password = data["password"]
            home = data["home"]

            # XXX consider error cases here
            self.db.addNewUser(email, password, home, name)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400 # Bad request


class NewUserListResource(GeneralResource):
    def on_post(self, req, resp):
        loggedInUser = verifyLoginAndGetUser(req.cookies)
        data = getReqJsonBody(req)
        if "name" in data and "members" in data:
            listID = self.db.addUserList(loggedInUser, data["name"])
            self.db.addUserListMembers(listID, data["members"])
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400


class SharingTargetsResource(GeneralResource):
    def on_get(self, req, resp, regex=""):
        loggedInUser = verifyLoginAndGetUser(req.cookies)
        userInfoObjs = self.db.getUsersByNameRegex(regex)
        listInfoObjs = self.db.getListsByNameRegex(loggedInUser, regex)
        for obj in listInfoObjs:
            obj["id"] = "#" + str(obj["id"])
        data = {"users" : userInfoObjs, "lists" : listInfoObjs}
        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_200


class UsersResource(GeneralResource):
    def on_get(self, req, resp, user=None):
        loggedInUser = verifyLoginAndGetUser(req.cookies)
        if not user:
            user = loggedInUser

        userInfo = self.db.getUserInfo(user)

        if not userInfo:
            resp.status = falcon.HTTP_404 # User not found
        else:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(userInfo)


class TravelNoticeResource(GeneralResource):
    # Argument "audience" is a list of user IDs
    def handleOverlaps(user, data):
        userContact = {} # Only fetch if necessary
        for friend in data["audience"]:
            overlaps = self.db.getTravelNoticeOverlaps(friend,
                                                       data["destination"],
                                                       data["start"],
                                                       data["end"])

            friendContact = {} # Only fetch these if we need them

            # TODO filter for those that overlap with user
            #overlaps = [] # TODO fill this list with friend's travel notices
                          # that overlap with this one of user's. Change travel
                          # times to only match time of overlap.

        #    for f in friendNotices:
        #        if f["start"] < data["end"] and data["start"] < f["end"]:
        #            # TODO match

            # TODO can we do all of this in the database? I think so, but
            # that's a problem for a later date. 
            for overlap in overlaps:
                visibilityList = self.db.getVisibilityByTravelNotice(overlap.id)
                if friendContact:
                    friendContact = self.db.getUserContactInfo(friend)
                if user in visibilityList:
                    if not userContact:
                        userContact = self.db.getUserContactInfo(user)
                    notify.send([friendContact, userContact], overlap)
                else:
                    notify.send([friendContact], overlap)

    def on_post(self, req, resp):
        user = verifyLoginAndGetUser(req.cookies)
        d = req.stream.read().decode("utf-8")
        print(d)
        data = json.loads(d)
        start = data["start"] # TODO decode timestamp?
        end = data["end"] # TODO decode another timestamp?

        # TODO check that all fields are actually included in object

        # TODO check for conflicts? Nope, better to do that in the front end
        # if we want to bother with it at all. 

        planID = self.db.addTravelNotice(user, data["destination"], start, end)

        # Handle notifications of possible overlaping schedules in background
        if "audience" in data and type(data["audience"]) == list:
            data["audience"] = self.convertAudience(data["audience"])
            background(self.handleOverlaps, (user, data))
            background(self.db.addVisibilityRow, (planID, data["audience"]))
        
        resp.status = falcon.HTTP_200



######
# Start everything up
#####

# Create a single database wrapper
dbwrapper = calldb.dbwrapper()

app = falcon.API()

app.add_route("/api/login", LoginResource(dbwrapper))
app.add_route("/api/new_travel_notice", TravelNoticeResource(dbwrapper))
app.add_route("/api/new_user", NewUserResource(dbwrapper))
app.add_route("/api/new_user_list", NewUserListResource(dbwrapper))
app.add_route("/api/sharing_targets/{regex}", SharingTargetsResource(dbwrapper))
app.add_route("/api/sharing_targets", SharingTargetsResource(dbwrapper))
app.add_route("/api/user_info/{user}", UsersResource(dbwrapper))
