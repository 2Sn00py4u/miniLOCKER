import sys, os
import json
import duck_dbms as db
import duck_functions as dbf

def logging(log:str, mode:str):
    with open("C:\\Users\\Felix\\Desktop\\coolStuff\\browser\\extensions\\L0ck3r\\nativeLog.txt", mode) as file:
            file.write(log)
            file.close()

def receiveMessage():
    #  reading message-head
    try:
        message_length = sys.stdin.buffer.read(4)
        if not message_length:
            return {"valid": False}
        message_length = int.from_bytes(message_length, byteorder='little')
        #logging(f"message_length: {message_length}\n", "a")
        #  reading message-body
        message = sys.stdin.buffer.read(message_length)
        loaded_message = json.loads(message.decode('utf-8'))
        loaded_message['valid'] = True
        #logging(f"loaded_message: {loaded_message}\n", "a")
        return loaded_message
    except:
        return {"valid": False}

def sendMessage(message):
    #  converting dict -> json
    json_message = json.dumps(message)
    encoded_message = json_message.encode('utf-8')
    #  writing message(message-head (first 4 bytes): length of message, message-body: json-message)
    sys.stdout.buffer.write(len(encoded_message).to_bytes(4, byteorder='little'))
    sys.stdout.buffer.write(encoded_message)
    #  send/flush message
    sys.stdout.buffer.flush()

def checkValidInput(uname: str, passwd: str):
    invalidChars = ['#', ',', '"', "'"]
    ValidInput = False
    if len(uname) >= 4 and len(uname) < 21 and len(passwd) >= 4 and len(passwd) < 21:
        if any(char in uname for char in invalidChars) == False and any(char in passwd for char in invalidChars) == False:
            ValidInput = True
    return ValidInput

def main():
    try:
        DBMS = db.DBMS(os.path.join(os.path.dirname(os.path.abspath(__name__)),r"l0ck3rdb.duckdb"))
        extensionPath = os.path.join(os.path.dirname(os.path.abspath(__name__)), r"dependencies\sqlite_scanner.duckdb_extension\sqlite_scanner.duckdb_extension")
        #logging(extensionPath, "a")
        DBMS.execute(f"LOAD '{extensionPath}'")
    except Exception as e:
        #logging(f"{str(e)}\n","w")
        sys.exit()
    try:    
        #logging("in loop\n", "a")
        received_message = receiveMessage()
        if received_message['valid'] == True:
            #logging("msg received\n", "a")
            #logging(f"received_message: {received_message}\n", "a")
            requestType = received_message['requestType']
            uname = received_message['uname']
            #logging(f"requestType: {requestType}\n", "a")
            if requestType == "logoutRequest":
                #logging("logging out...\n", "a")
                userdata = dbf.readUserdata(DBMS, uname)
                #logging(f"userdata: {userdata}\n", "a")
                if userdata != None:
                    userdata["latest_access"] = received_message['timestamp']
                    dbf.setUserdata(DBMS, uname, userdata)
                    sendMessage({"logout": True})
                    #logging(f"logout\n", "a")
                    
            elif requestType == "deleteAccountRequest":
                #logging("logging out...\n", "a")
                userdata = dbf.readUserdata(DBMS, uname)
                #logging(f"userdata: {userdata}\n", "a")
                if userdata != None:
                    dbf.deleteUser(DBMS, uname)
                    sendMessage({"accountDelete": True})
                    #logging(f"logout\n", "a")
                      
            elif requestType == "delete_passwordCard":
                #logging("deleting card...\n", "a")
                userdata = dbf.readUserdata(DBMS, uname)
                if userdata != None:
                    for i in range(len(userdata["password_cards"])):
                        #logging(f"{userdata["password_cards"][i]}\n {received_message["password_card"]}\n","a")
                        #logging(f"{str(userdata["password_cards"][i] == received_message["password_card"])}\n", "a")
                        if userdata["password_cards"][i] == received_message["password_card"]:
                            userdata["password_cards"].pop(i)
                            #logging("1\n","a")
                            for i in range(len(userdata["password_cards"])):
                                userdata["password_cards"][i]["card_id"] = str((i+1))
                            #logging("2\n","a")
                            dbf.setUserdata(DBMS, uname, userdata)
                            sendMessage({"deletedPasswordCard": True})
                            #logging(f"deleted{userdata["password_cards"][i]}", "a")
                            break
                                            
            elif requestType == "edit_passwordCard":
                #logging("editing card...\n", "a")
                userdata = dbf.readUserdata(DBMS, uname)
                if userdata != None:
                    for i in range(len(userdata["password_cards"])):
                        #logging(f"{userdata["password_cards"][i]}\n {received_message["password_card"]}\n","a")
                        #logging(f"{str(userdata["password_cards"][i] == received_message["password_card"])}\n", "a")
                        if userdata["password_cards"][i]["card_id"] == received_message["password_card"]["card_id"]:
                            userdata["password_cards"][i]["email"] = received_message["password_card"]["email"]
                            userdata["password_cards"][i]["password"] = received_message["password_card"]["password"]
                            userdata["password_cards"][i]["img_path"] = received_message["password_card"]["img_path"]
                            edited = True
                            if userdata["password_cards"][i]["card_title"] == "L0CK3R":
                                edited = dbf.updateLogin(DBMS, uname, received_message["password_card"]["email"], received_message["password_card"]["password"])
                                if edited == False:
                                    sendMessage({"editPasswordCard": edited, "uname": userdata["user"]})
                                    #logging(f"edited: {edited}\n","a")
                                    #logging(f'editPasswordCard: {edited}\nuname: {userdata["user"]}', "a")
                                    break
                                userdata["user"] = received_message["password_card"]["email"]
                                uname = received_message["password_card"]["email"]
                                 
                            #logging("1\n","a")
                            setted = dbf.setUserdata(DBMS, uname, userdata)
                            #logging(f"{str(setted)} -- uname {uname}\n","a")
                            #logging(f"edited: {edited}\n","a")
                            sendMessage({"editPasswordCard": edited, "uname": userdata["user"]})
                            #logging(f"edited{userdata}", "a")
                            #logging(f"reading userdata: {dbf.readUserdata(DBMS, uname)}\n", "a")
                            break
                        
            elif requestType == "add_passwordCard":
                #logging("adding card...\n", "a")
                userdata = dbf.readUserdata(DBMS, uname)
                if userdata != None:
                    new_card = {
                        "card_id": received_message["password_card"]["card_id"],
                        "card_title": received_message["password_card"]["card_title"],
                        "img_path": received_message["password_card"]["img_path"],
                        "email": received_message["password_card"]["email"],
                        "password": received_message["password_card"]["password"],
                    }
                    userdata["password_cards"].append(new_card)
                    added = dbf.setUserdata(DBMS, uname, userdata)
                    sendMessage({"addedPasswordCard": added})
                    #logging(f"added{userdata}\n", "a")
            else:
                passwd = received_message['passwd']
                #logging(f"{requestType}\nuname:{uname}\npasswd:{passwd}\n", "a")
                if checkValidInput(uname, passwd) == True:
                    if requestType == "loginRequest":
                        response = {
                            "received": [uname, passwd],
                            "access": dbf.L0CKin(DBMS, uname, passwd),
                        }
                        if response["access"] == True:
                            #logging("\nACCESS == True\n", "a")
                            response["userdata"] = dbf.readUserdata(DBMS, uname)
                            #logging(f"\nresponse['userdata']  UPDATE\n\n?{dbf.readUserdata(DBMS, uname)}?\n\n", "a")
                        else:
                            sendMessage({"access": False})
                            #logging(f"user not registered: {received_message}\n", "a")
                        
                    elif requestType == "registerRequest":
                        response = {
                            "received": [uname, passwd],
                            "access": dbf.R3gister(DBMS, uname, passwd)
                        }
                        if response["access"] == True:
                            standard_userdata = {
                                "user": uname,
                                "latest_access": "new",
                                "password_cards": [
                                    {
                                        "card_id": "1",
                                        "card_title": "L0CK3R",
                                        "img_path": "../assets/icons/icon128.png",
                                        "email": uname,
                                        "password": passwd,
                                    }
                                ]
                            }
                            dbf.setUserdata(DBMS, uname, standard_userdata)
                            response["userdata"] = dbf.readUserdata(DBMS, uname)
                    #logging(f"\n GOING TO SEND RESPONSE \n{response}\n\n{type(response)}\n\n", "a")    
                    sendMessage(response)
                    
                    #logging(f"succesfully send: {response["received"]}\n access: {response["access"]}\n", "a")
                else:
                    sendMessage({"access": False})
                    #logging(f"Invalidsend: {received_message}\n", "a")
        else:
            try:
                sendMessage({"access": False})
                #logging(f"Invalidsend: {received_message}\n", "a")
            except:
                pass

    except Exception as e:        
        #logging(f"Disconnected\nerror: {e}\n{e.args}\n", "a")
        sys.exit()
    finally:
        DBMS.disconnectDB()
        #logging("DBMS disconnected\n", "a")
        
if __name__ == "__main__":
    main()
