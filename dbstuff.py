def checkPostTableExists(dbcon):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'posts'
        """)
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

def setupDB(dbcon):
    # read db.sql file and execute it
    with open('db.sql', 'r') as f:
        sql = f.read()
        statements = sql.split(';')
        for statement in statements:
            print(statement)
            
            dbcur = dbcon.cursor()
            dbcur.execute(statement)
            dbcon.commit()
            dbcur.close()
        

def insertUser(dbcon,user):
    id = user['user']['id']
    currentName = user['user']['name']
    registered = user['user']['registered']
    score = user['user']['score']
    uploadCount = user['uploadCount']

    dbcur = dbcon.cursor()
    dbcur.execute("""
        INSERT INTO users 
        (id,currentName,registered,uploadCount,score)
        VALUES (%s,%s,%s,%s,%s)
        """,(id,currentName,registered,uploadCount,score))
    dbcon.commit()
    dbcur.close()
        
def insertPost(dbcon,post):

    id = post['id']
    userId = post['userId']
    up = post['up']
    down = post['down']
    created = post['created']
    width = post['width']
    height = post['height']
    audio = post['audio']
    flags = post['flags']

    dbcur = dbcon.cursor()
    dbcur.execute("""
        INSERT INTO posts 
        (id,userId,up,down,created,width,height,audio,flags)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,(id,userId,up,down,created,width,height,audio,flags))
    dbcon.commit()
    dbcur.close()

def insertComment(dbcon,comment,postId,userId):
    id = comment['id']
    parentId = comment['parent']
    up = comment['up']
    down = comment['down']
    created = comment['created']
    content = comment['content']

    dbcur = dbcon.cursor()
    dbcur.execute("""
        INSERT INTO comments 
        (id,postId,parentId,userId,up,down,created,content)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,(id,postId,parentId,userId,up,down,created,content))
    dbcon.commit()
    dbcur.close()

def insertTag(dbcon,tag):
    
    tagName = tag['tag']

    dbcur = dbcon.cursor()
    dbcur.execute("""
        INSERT INTO tags 
        (name)
        VALUES (%s)
        """,[tagName])
    dbcon.commit()
    dbcur.close()

def insertBadge(dbcon,badge):
    image = badge['image']

    dbcur = dbcon.cursor()
    dbcur.execute("""
        INSERT INTO badges 
        (image)
        VALUES (%s)
        """,[image])
    dbcon.commit()
    dbcur.close()

def getIdForBadgeByImage(dbcon,badge):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT id
        FROM badges
        WHERE image = %s
        """,[badge['image']])
    id = dbcur.fetchone()[0]
    dbcur.close()
    return id

def connectTagToPost(dbcon,tagId,postId,confidence):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        INSERT INTO post_tags
        (postId,tagId,confidence)
        VALUES (%s,%s,%s)
        """,(postId,tagId,confidence))
    dbcon.commit()
    dbcur.close()

def connectBadgeToUser(dbcon,badgeId,userId):

    dbcur = dbcon.cursor()
    dbcur.execute("""
        INSERT INTO user_badges 
        (userId,badgeId)
        VALUES (%s,%s)
        """,(userId,badgeId))
    dbcon.commit()
    dbcur.close()

def checkForUser(dbcon,user):
    #check if user exists
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE id = %s
        """,[user['user']['id']])
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False

def checkForPost(dbcon,post):
    #check if post exists
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM posts
        WHERE id = %s
        """,[post['id']])
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False

def checkForComment(dbcon,comment):
    #check if comment exists
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM comments
        WHERE id = %s
        """,[comment['id']])
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False

def checkForTag(dbcon,tag):
    #check if tag exists
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM tags
        WHERE name = %s
        """,[tag['tag']])
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False

def getIdFortagName(dbcon,tag):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT id
        FROM tags
        WHERE name = %s
        """,[tag['tag']])
    id = dbcur.fetchone()[0]
    dbcur.close()
    return id

def checkForBadge(dbcon,badge):
    #check if badge exists
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM badges
        WHERE image = %s
        """,[badge['image']])
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False

def checkForConnectionTagToPost(dbcon,tagId,postId):
    #check if connection exists
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM post_tags
        WHERE postId = %s AND tagId = %s
        """,(postId,tagId))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False

def checkForConnectionBadgeToUser(dbcon,badgeId,userId):
    #check if connection exists
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM user_badges
        WHERE userId = %s AND badgeId = %s
        """,(userId,badgeId))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False    

def updateUser(dbcon,user):
    id = user['user']['id']
    currentName = user['user']['name']
    registered = user['user']['registered']
    score = user['user']['score']
    uploadCount = user['uploadCount']

    dbcur = dbcon.cursor()
    dbcur.execute("""
        UPDATE users
        SET currentName = %s, registered = %s, score = %s, uploadCount = %s
        WHERE id = %s
        """,(currentName,registered,score,uploadCount,id))
    dbcon.commit()
    dbcur.close()

def updatePost(dbcon,post):
    id = post['id']
    userId = post['userId']
    up = post['up']
    down = post['down']
    created = post['created']
    width = post['width']
    height = post['height']
    audio = post['audio']
    flags = post['flags']

    dbcur = dbcon.cursor()
    dbcur.execute("""
        UPDATE posts
        SET userId = %s, up = %s, down = %s, created = %s, width = %s, height = %s, audio = %s, flags = %s
        WHERE id = %s
        """,(userId,up,down,created,width,height,audio,flags,id))
    dbcon.commit()
    dbcur.close()

def updateComment(dbcon,comment):
    id = comment['id']
    parentId = comment['parent']
    up = comment['up']
    down = comment['down']
    created = comment['created']
    content = comment['content']

    dbcur = dbcon.cursor()
    dbcur.execute("""
        UPDATE comments
        SET parentId = %s, up = %s, down = %s, created = %s, content = %s
        WHERE id = %s
        """,(parentId,up,down,created,content,id))
    dbcon.commit()
    dbcur.close()

def updateConnectionTagToPost(dbcon,tagId,postId,confidence):
    
    dbcur = dbcon.cursor()
    dbcur.execute("""
        UPDATE post_tags
        SET confidence = %s
        WHERE postId = %s AND tagId = %s
        """,(confidence,postId,tagId))
    dbcon.commit()
    dbcur.close()

def getAuthorIdByName(dbcon,user):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT id
        FROM users
        WHERE currentName = %s
        """,(user))
    id = dbcur.fetchone()[0]
    dbcur.close()
    return id