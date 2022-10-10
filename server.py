
import sqlite3

connect = sqlite3.connect('subsc.db', check_same_thread=False)
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL	
);""")
connect.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS "subscribes" (
	"user_id"	INTEGER NOT NULL,
	"category_id"	INTEGER NOT NULL,
	PRIMARY KEY("user_id","category_id")
);""")
connect.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER NOT NULL,
	"name"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")
connect.commit()


def fillCateg(arrCateg):
    i = 0
    while i < (len(arrCateg)):
        res = cursor.execute("""SELECT categories.name FROM categories WHERE name=:name""",
                             {"name": arrCateg[i]}).fetchone()
        if res == None:
            cursor.execute("""INSERT INTO categories (name) VALUES (:name)""", {"name": arrCateg[i]})
            connect.commit()
        i+=1

def checkSub(message,cat_id):
    cat_id+=1
    return cursor.execute("""SELECT user_id, category_id FROM subscribes WHERE user_id=:user_id AND category_id=:cat_id""",
                   {"user_id": message.from_user.id, "cat_id": cat_id}).fetchone()

def addUser(id):
    result = cursor.execute("""SELECT users.id FROM users WHERE id=:id""", {"id": id}).fetchone()
    if result == None:
        cursor.execute("""INSERT INTO users (id) VALUES (:id)""", {"id": id})
        connect.commit()

def subInfo(message):
    result = cursor.execute("""SELECT categories.name FROM categories, subscribes WHERE subscribes.user_id LIKE :user_id AND subscribes.category_id == categories.id""",
        {"user_id": message.from_user.id}).fetchall()
    arr=[]
    for i in result:
        arr.append(i[0])
    return arr


def subUser(message, cat_id):
    addUser(message.from_user.id)
    # result = cursor.execute("""SELECT user_id, category_id FROM subscribes WHERE user_id=? AND category_id=?""" , (message.from_user.id,cat_id)).fetchone()
    result = cursor.execute(
        """SELECT user_id, category_id FROM subscribes WHERE user_id=:user_id AND category_id=:cat_id""",
        {"user_id": message.from_user.id, "cat_id": cat_id}).fetchone()

    if result == None:
        cursor.execute("""INSERT INTO subscribes (user_id, category_id) VALUES (:user_id, :cat_id)""",
                       {"user_id": message.from_user.id, "cat_id": cat_id})
        connect.commit()
        return True
    else:
        return False

def unsubUser(message, cat_id):
    addUser(message.from_user.id)
    result = cursor.execute("""SELECT user_id, category_id FROM subscribes WHERE user_id=:user_id AND category_id=:cat_id""",
                            {"user_id": message.from_user.id, "cat_id": cat_id}).fetchone()
    if result != None:
        cursor.execute("""DELETE FROM subscribes WHERE category_id=:cat_id and user_id=:user_id""", {"cat_id": cat_id, "user_id": message.from_user.id})
        connect.commit()
        return True
    else:
        return False




