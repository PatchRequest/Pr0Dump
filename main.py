
import os
from dotenv import load_dotenv
import mysql.connector
from helper import loginUser,registerPost
from dbstuff import *
from pr0Requests import *
import time


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
    latestID = 4080832 
    nextPosts = getNextXPosts(latestID,x.cookies)

    while latestID > 2:
        
        for post in nextPosts:

            try:
                tags, comments = getTagsAndCommentsOfPost(post['id'],x.cookies)
                authorData = getUserDetails(post['user'],x.cookies)
                registerPost(mydb,authorData,authorData['user']['id'],post,tags,comments,authorData['badges'])
            except Exception as e:
                # open file error.txt and add the error with timestamp
                print("[-] Error with post: " + str(post['id']))
                print(e)
                with open("error.txt", "a") as myfile:
                    myfile.write(str(post['id']) + " " + str(e) + post + "\n")
                continue


        latestID = nextPosts[-1]['id']

        try:
            nextPosts = getNextXPosts(latestID,x.cookies)
        except Exception as e:
            print("[-] Error with getting next posts")
            print(e)
            with open("error.txt", "a") as myfile:
                myfile.write(str(e) + "\n")
            time.sleep(600)
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