import requests
from dbstuff import *
from pr0Requests import *

def loginUser(username,password):
    print("[*] Loggin in for user: " + username)
    token, captchaSolution= solveCaptche()
    data = {
        "name":username,
        "password":password,
        "token":token,
        "captcha":captchaSolution
    }
    x = requests.post('https://pr0gramm.com/api/user/login', data=data)
    print("[+] Logged in for user: " + username)
    return x
    
def solveCaptche():
    print("[*] Requesting Captcha")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    x = requests.get('https://pr0gramm.com/api/user/captcha',headers=headers)
    xJson = x.json()
    
    token = xJson['token']
    captache = xJson['captcha']
    print(captache)
    captchaSolution = input("Captcha: ")

    return token, captchaSolution

def registerPost(mydb,authorData,authorID,post,tags,comments,badges):

    insertOrUpdateUser(mydb,authorData)
    print("[+] Updated User, ID: " + str(authorID))


    insertOrUpdatePost(mydb,post)
    print("[+] Updated Post, ID: " + str(post['id']))


    # For every comment
    for comment in comments:
        insertOrUpdateComment(mydb,comment,post['id'],authorID)
        print("[+] Updated Comment, ID: " + str(comment['id']))

    # For every tag
    for tag in tags:
        tagId = 0
        # Check if tag exists
        if checkForTag(mydb,tag):
            # Get internal tag id
            tagId = getIdFortagName(mydb,tag)
        else:
            # Insert tag information
            insertTag(mydb,tag)
            tagId = getIdFortagName(mydb,tag)
            print("[+] New Tag, ID: " + str(tagId))

        connectOrUpdateTagToPost(mydb,tagId,post['id'],tag['confidence'])
        print("[+] Updated Connection Tag to Post, ID: " + str(tagId))

    # For every badge
    for badge in badges:
        badgeId = 0

        # Check if badge exists
        if checkForBadge(mydb,badge):
            # Get internal badge id
            badgeId = getIdForBadgeByImage(mydb,badge)
        else:
            # Insert badge information
            insertBadge(mydb,badge)
            badgeId = getIdForBadgeByImage(mydb,badge)
            print("[+] New Badge, ID: " + str(badgeId))
        
        # Check if badge is already connected to user
        if not checkForConnectionBadgeToUser(mydb,badgeId,authorID):
            # Insert badge connection
            connectBadgeToUser(mydb,badgeId,authorID)
            print("[+] New Connection Badge to User, ID: " + str(badgeId))