import urllib, urllib2, json
from pprint import pprint

# important functions

def authenticate(FBTOKEN, FBID):
    url = "https://api.gotinder.com/auth"
    values = {"facebook_token": FBTOKEN, "facebook_id": FBID}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def postForm(url, data, token):
    postURL = "https://api.gotinder.com/" + url
    postData = urllib.urlencode(data)
    req = urllib2.Request(postURL, postData)
    req.add_header("X-Auth-Token", token)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def sendMessage(to, message, token):
    url = 'user/matches/' + to 
    data = {"message": message}
    pprint(postForm(url, data, token))
    print "\n"
