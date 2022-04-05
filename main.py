
import os
from dotenv import load_dotenv
import mysql.connector
from helper import loginUser
from dbstuff import *
from pr0Requests import *



def main():
    USERNAME, PASSWORD, DBHOST, DBUSER, DBPASS, DBNAME = loadEnv()
    mydb = mysql.connector.connect(
        host=DBHOST,
        user=DBUSER,
        password=DBPASS,
        database=DBNAME
    )
    if(not checkPostTableExists(mydb)):
        setupDB(mydb)

    x = loginUser(USERNAME, PASSWORD)

    latestID = getLatestPostID(x.cookies)
    nextPosts = getNextXPosts(latestID,x.cookies)

    while latestID > 2:
        
        for post in nextPosts:
            comments = getCommentsOfPost(post['id'],x.cookies)
            tags = getTagsOfPost(post['id'],x.cookies)
            
            authorData = getUserDetails(post['user'],x.cookies)
            authorID = authorData['user']['id']

            if checkForUser(mydb,authorData):
                #print("[*] User already in DB, ID: " + str(authorID))
                updateUser(mydb,authorData)
            else:
                print("[+] New User, ID: " + str(authorID))
                insertUser(mydb,authorData)

            if checkForPost(mydb,post):
                #print("[*] Post already in DB, ID: " + str(post['id']))
                updatePost(mydb,post)
            else:
                print("[+] New Post, ID: " + str(post['id']))
                insertPost(mydb,post)
 
            

            for comment in comments:
                if checkForComment(mydb,comment):
                    #print("[*] Comment already in DB, ID: " + str(comment['id']))
                    updateComment(mydb,comment)
                else:
                    insertComment(mydb,comment,post['id'],authorID)
                    print("[+] New Comment, ID: " + str(comment['id']))

            for tag in tags:
                tagId = 0
                
                if checkForTag(mydb,tag):
                    tagId = getIdFortagName(mydb,tag)
                    #print("[*] Tag already in DB, ID: " + str(tagId))
                else:
                    insertTag(mydb,tag)
                    tagId = getIdFortagName(mydb,tag)
                    print("[+] New Tag, ID: " + str(tagId))


                

                if checkForConnectionTagToPost(mydb,tagId,post['id']):
                    #print("[*] Connection Tag to Post already in DB, ID: " + str(tagId))
                    updateConnectionTagToPost(mydb,tagId,post['id'],tag['confidence'])
                else:
                    connectTagToPost(mydb,tagId,post['id'],tag['confidence'])
                    print("[+] New Connection Tag to Post, ID: " + str(tagId))


            for badge in authorData['badges']:
                badgeId = 0

                if checkForBadge(mydb,badge):
                    badgeId = getIdForBadgeByImage(mydb,badge)
                    #print("[*] Badge already in DB, ID: " + str(badgeId))
                else:
                    insertBadge(mydb,badge)
                    badgeId = getIdForBadgeByImage(mydb,badge)
                    print("[+] New Badge, ID: " + str(badgeId))
                
                if checkForConnectionBadgeToUser(mydb,badgeId,authorID):
                    pass
                    #print("[*] Connection Badge to User already in DB, ID: " + str(badgeId))
                else:
                    connectBadgeToUser(mydb,badgeId,authorID)
                    print("[+] New Connection Badge to User, ID: " + str(badgeId))

        latestID = nextPosts[-1]['id']
        nextPosts = getNextXPosts(latestID,x.cookies)




def loadEnv():
    load_dotenv()
    USERNAME = os.getenv('USERNAMEPRO')
    PASSWORD = os.getenv('PASSWORD')
    DBHOST = os.getenv('DBHOST')
    DBUSER = os.getenv('DBUSER')
    DBPASS = os.getenv('DBPASS')
    DBNAME = os.getenv('DBNAME')
    return USERNAME, PASSWORD, DBHOST, DBUSER, DBPASS, DBNAME

if __name__ == '__main__':
    main()