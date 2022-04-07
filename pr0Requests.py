import requests


def getUserDetails(name,cookie):

    x = requests.get('https://pr0gramm.com/api/profile/info?name='+name+'&flags=15',cookies=cookie)
    xJson = x.json()
    print("[+] Got User Details about {}".format(name))
    return xJson

def getLatestPostID(cookie):

    x = requests.get('https://pr0gramm.com/api/items/get?flags=15',cookies=cookie)
    xJson = x.json()
    xArray = xJson['items']
    print("[+] Current highest ID is: {}".format(xArray[0]['id']))
    return xArray[0]['id']


def getNextXPosts(startId,cookie):
    print("[*] Getting Posts from {}".format(startId))
    x = requests.get('https://pr0gramm.com/api/items/get?older={}&flags=15'.format(startId),cookies=cookie)
    xJson = x.json()
    xArray = xJson['items']
    print("[+] Found {} Posts".format(len(xArray)))
    return xArray

def getTagsOfPost(id,cookie):
    x = requests.get('https://pr0gramm.com/api/items/info?itemId={}'.format(id),cookies=cookie)
    try:
        tags = x.json()['tags']
    except:
        tags = []
    print("[+] Found {} Tags for Post {}".format(len(tags),id))
    return tags

def getCommentsOfPost(id,cookie):
    x = requests.get('https://pr0gramm.com/api/items/info?itemId={}'.format(id),cookies=cookie)
    try:
        comments = x.json()['comments']
    except:
        comments = []
    print("[+] Found {} Comments for Post {}".format(len(comments),id))
    return comments