#######
# Module to handle notifications
#######

import json
import pywebpush




def getFromFile(path):
    with open(path, "r") as f:
        contents = f.read()
    return contents.strip()




# to: [ { "email" : "...", "phone" : "...", ... }, ... ]
def send(to, message):
    private_key = getFromFile("webpush.key")
    for userdata in to:
        for push_subscription in userdata["push"]:
            pywebpush.webpush(push_subscription,
                              json.dumps(message),
                              vapid_private_key=private_key,
                              vapid_claims={
                                  "sub" : "mailto:kechpaja@comcast.net"
                              })




def overlap(to, obj):
    send(to, {"type" : "overlap", "data" : obj})
