try:
    import backend.duck_dbms as db
    import backend.crypting as cy
except ImportError:
    import duck_dbms as db
    import crypting as cy   
import base64 as b64
import json
from datetime import date


USERDATA = {
    "user": "admin",
    "latest_access": str(date.today()),
    "password_cards": [
        {
            "card_id": "1",
            "website": "www.L0CK3R.com",
            "email": "admin",
            "password": "admin"
        }
    ]
}

def connect_L0CKER_DB(filePath: str) -> db.DBMS:
    return db.DBMS(filePath)

def build_L0CK3R_DB(filePath: str) -> db.DBMS:
    L0CK3R_DBMS = db.DBMS(filePath)
    tables = L0CK3R_DBMS.getTables()
    for table in tables:
        try:
            L0CK3R_DBMS.deleteTable(table)
        except:
            pass
       
    #  users(_id_, uname, passwd, registerDate)
    L0CK3R_DBMS.createTable("users",["username VARCHAR PRIMARY KEY NOT NULL", "password BLOB", "registerDate VARCHAR NOT NULL", "userdata JSON"])
    R3gister(L0CK3R_DBMS, "admin", "admin")
    return L0CK3R_DBMS

def L0CKin(DBMS: db.DBMS, username: str, password: str) -> bool:
    L0CK3R_DBMS = DBMS
    l0ck3din = False
    result = L0CK3R_DBMS.execute(f"""SELECT * FROM users WHERE username = '{username}'""")
    if result != []:
        userpassword = L0CK3R_DBMS.execute(f"""SELECT password FROM users WHERE username = '{username}'""")[0][0]
        l0ck3din = cy.compare_encrypted(password, password, userpassword)
    return l0ck3din
    
    
def R3gister(DBMS: db.DBMS, username: str, password: str) -> bool:
    L0CK3R_DBMS = DBMS
    try:
        L0CK3R_DBMS.insertValues("users",[(username, cy.encrypting(password, password), str(date.today()), {})])
        setUserdata(L0CK3R_DBMS, username, {"user": "admin",
            "latest_access": str(date.today()),
            "password_cards": [
                {
                    "card_id": "1",
                    "website": "www.L0CK3R.com",
                    "email": username,
                    "password": password
                }
        ]})
        r3gistert = True
    except Exception as e:
        r3gistert = False
    return r3gistert

def updateLogin(DBMS: db.DBMS, username: str, new_username: str, password: str) -> bool:
    L0CK3R_DBMS = DBMS
    try:
        L0CK3R_DBMS.execute(f"""UPDATE users SET password = ? WHERE username = ?""", False, cy.encrypting(password, password), username)
        L0CK3R_DBMS.execute(f"""UPDATE users SET username = ? WHERE username = ?""", False, new_username, username)
        return True
    except Exception as e:
        return False

def readUserdata(DBMS: db.DBMS, username: str, pdOutput: bool = False) -> dict:
    L0CK3R_DBMS = DBMS
    try:
        user_data = L0CK3R_DBMS.execute(f"""SELECT userdata FROM users WHERE username = '{username}'""", pdOutput)
        if pdOutput == False:
            if user_data != []:
                fetched_user = json.loads(user_data[0][0])
                for i in range(len(fetched_user["password_cards"])):
                    fetched_user["password_cards"][i]["password"] = b64.b64decode(fetched_user["password_cards"][i]["password"].encode("utf-8"))
                    fetched_user["password_cards"][i]["password"] = cy.decrypting(fetched_user["password_cards"][i]["password"], fetched_user["password_cards"][i]["email"])
        else:
            return user_data           
                    
    except Exception as e:
        print(e)
    return fetched_user

def setUserdata(DBMS: db.DBMS, username: str, userdata: dict) -> bool:
    L0CK3R_DBMS = DBMS
    try:
        for i in range(len(userdata["password_cards"])):
            userdata["password_cards"][i]["password"] = b64.b64encode(cy.encrypting(userdata["password_cards"][i]["password"], userdata["password_cards"][i]["email"])).decode("utf-8")
        L0CK3R_DBMS.execute(f"""UPDATE users SET userdata = '{json.dumps(userdata)}' WHERE username = '{username}'""")
        return True
    except Exception as e:
        print(e)
        return False

def deletePasswordCard(DBMS: db.DBMS, username: str, website) -> bool:
    L0CK3R_DBMS = DBMS
    try:
        userdata = readUserdata(L0CK3R_DBMS, username)
        for i in range(len(userdata["password_cards"])):
            if userdata["password_cards"][i]["website"] == website:
                del userdata["password_cards"][i]
                break
        setUserdata(L0CK3R_DBMS, username, userdata)
        return True
    except Exception as e:
        print(e)
        return False
    
def editPasswordCard(DBMS: db.DBMS, username: str, card_id: str, new_username: str, new_password: str) -> bool:
    L0CK3R_DBMS = DBMS
    try:
        userdata = readUserdata(L0CK3R_DBMS, username)
        for i in range(len(userdata["password_cards"])):
            if userdata["password_cards"][i]["card_id"] == card_id:
                userdata["password_cards"][i]["email"] = new_username
                userdata["password_cards"][i]["password"] = new_password
                break
        setUserdata(L0CK3R_DBMS, username, userdata)
        return True
    except Exception as e:
        print(e)
        return False

def deleteUser(DBMS: db.DBMS, username: str):
    L0CK3R_DBMS = DBMS
    try:
        DBMS.deleteValues("users", f"username = '{username}'")
        return True
    except:
        return False

def closeConnection(DBMS: db.DBMS) -> None:
    DBMS.disconnectDB()
    
"""
DMBS = db.DBMS("backend\\l0ck3rdb.duckdb")
print(deleteUser(DMBS, "user"))"""
#DBMS = build_L0CK3R_DB("backend\\l0ck3rdb.duckdb")
#print(readUserdata(DBMS, "toni"), type(readUserdata(DBMS, "toni")))   
"""
DBMS = build_L0CK3R_DB("backend\\l0ck3rdb.duckdb")


#print(readUserdata(DBMS, "admin"),type(readUserdata(DBMS, "admin")))

USERDATA["password_cards"].append(
    {
        "card_id": "2",
        "website": "www.youtube.com",
        "email": "admin@youtube.com",
        "password": "YTadmin123",
    }
)
USERDATA["password_cards"].append(
    {
        "card_id": "3",
        "website": "www.google.com",
        "email": "admin@google.com",
        "password": "googleAdmin123",
    }
)
USERDATA["password_cards"].append(
    {
        "card_id": "4",
        "website": "www.instagram.com",
        "email": "admin@instagram.com",
        "password": "instaAdmin123",
    }
)
USERDATA["password_cards"].append(
    {
        "card_id": "5",
        "website": "www.spotify.com",
        "email": "admin@spotify.com",
        "password": "spotiAdmin123",
    }
)



print(setUserdata(DBMS, "admin", USERDATA))

print(readUserdata(DBMS, "admin"),type(readUserdata(DBMS, "admin")))

print(L0CKin(DBMS, "admin", "admin"))
print(L0CKin(DBMS, "admin", "wrongpassword"))
print(R3gister(DBMS, "admin1", "admin1"))
print(L0CKin(DBMS, "admin1", "admin1"))
print(L0CKin(DBMS, "admin1", "wrongpassword"))
print(updateLogin(DBMS, "admin", "admin2", "admin2"))
print(L0CKin(DBMS, "admin2", "admin2"))

print(readUserdata(DBMS, "admin2"))"""