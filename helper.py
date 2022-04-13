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
    # Check if user exists
    if checkForUser(mydb,authorData):
        # Update user information
        updateUser(mydb,authorData)
    else:
        # Insert user information
        print("[+] New User, ID: " + str(authorID))
        insertUser(mydb,authorData)

    # Check if post exists
    if checkForPost(mydb,post):
        # Update post information
        updatePost(mydb,post)
    else:
        # Insert post information
        print("[+] New Post, ID: " + str(post['id']))
        insertPost(mydb,post)

    # For every comment
    for comment in comments:
        # Check if comment exists
        if checkForComment(mydb,comment):
            # Update comment information
            updateComment(mydb,comment)
        else:
            # Insert comment information
            print("[+] New Comment, ID: " + str(comment['id']))
            insertComment(mydb,comment,post['id'],authorID)
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

        # Check if tag is already connected to post
        if checkForConnectionTagToPost(mydb,tagId,post['id']):
            # Update tag connection
            updateConnectionTagToPost(mydb,tagId,post['id'],tag['confidence'])
        else:
            # Insert tag connection
            print("[+] New Connection Tag to Post, ID: " + str(tagId))
            connectTagToPost(mydb,tagId,post['id'],tag['confidence'])
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