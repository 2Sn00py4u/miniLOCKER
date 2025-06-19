import duck_functions as dbf
import sys, pandas as pd

def main():
    running = True
    login = False
    register = False
    wrongCount = 0
    username = ""
    password = ""
    DBMS = dbf.connect_L0CKER_DB(r"backend/l0ck3rdb.duckdb")
    print("Bulding miniL0CK3R...")
    while running: 
        if login:
            cmd = input("enter command: ")
            if cmd[:10] == "show pass:":
                if cmd[10:] == "all":
                    for i in range(len(userdata["password_cards"])):
                        print(userdata["password_cards"][i])
                else:
                    title = cmd[10:].lower()
                    for i in range(len(userdata["password_cards"])):
                        if userdata["password_cards"][i]["card_title"].lower() == title:
                            print(userdata["password_cards"][i])
                            break       
                    
            elif cmd == "logout":
                login = False
            elif cmd == "exit":
                print("closing DB...")
                dbf.closeConnection(DBMS)
                sys.exit()

        elif register:
            print("Register\n")
            username = input("Benutzername: ")
            password = input("Passwort: ")
            login = dbf.R3gister(DBMS, username, password)
            if login == True:
                print(f"Welcome back, {username}!")
                userdata = dbf.readUserdata(DBMS, username)
                print(f"latest access: {userdata["latest_access"]}")
            else:
                print(f"Username already in use!\nTry again ({3-wrongCount} remaining)")
                wrongCount += 1
                if wrongCount >= 3:
                    print("Danger!!\nClosing and DB")
                    sys.exit()
        else:
            print("Login\n")
            username = input("Benutzername: ")
            password = input("Passwort: ")
            if username == "r" and password == "":
                register = True   
            else:
                login = dbf.L0CKin(DBMS, username, password)
                if login == True:
                    print(f"Welcome back, {username}!")
                    userdata = dbf.readUserdata(DBMS, username)
                    print(f"latest access: {userdata["latest_access"]}")
                else:
                    print(f"Wrong username or password provided!\nTry again ({3-wrongCount} remaining)")
                    wrongCount += 1
                    if wrongCount >= 3:
                        print("Danger!!\nClosing and DB")
                        sys.exit()
                    

if __name__ == "__main__":
    main()