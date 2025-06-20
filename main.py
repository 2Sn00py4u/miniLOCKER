import customtkinter as ctk
import tkinter.messagebox as mbox
import tldextract
import backend.duck_functions as dbf
import sys
import pyperclip as clip


class PasswordFrame(ctk.CTkFrame):
    def __init__(self, master, id: str, website: str, username: str, password: str, uncensor: bool) -> None:
        """
        Vor.: Variablen: master, id, website, username, password, uncensor
        Eff.: Eine Objekt der Klasse PasswordFrame wird gespeichert
        Erg.: Objekt der Klasse PasswordFrame mit den Attributen id, website, username, password und uncensor wird erstellt
        """
        super().__init__(master)
        self.__id = id
        self.website = website
        self.username = username
        self.password = password

        if uncensor == False:
            password_text = "*" * len(self.password)

        else:
            password_text = self.password

        self.grid_rowconfigure(0, weight= 1)
        self.grid_columnconfigure(0, weight= 2)
        self.grid_columnconfigure(1, weight= 1)

        domain = tldextract.extract(website)

        self.title = ctk.CTkLabel(self, text = domain.top_domain_under_public_suffix, corner_radius = 10, fg_color = "blue", pady= 10, padx = 10 )
        self.title.grid(row = 0, column = 0, columnspan= 2, sticky = "ew")

        self.text1 = ctk.CTkLabel(self, text = f"Username: {username}", padx=10, fg_color="grey30", pady = 5, anchor = "w")
        self.text1.grid(row = 1, column = 0, columnspan= 2 , sticky = "we")

        optFrame = ctk.CTkFrame(self, width=200, corner_radius=10, bg_color="grey20")
        optFrame.grid(row = 2, column = 1, sticky = "ew")
        
        optFrame.grid_columnconfigure(1, weight=1)
        optFrame.grid_rowconfigure(0, weight=1)

        self.censorbox = ctk.CTkCheckBox(optFrame, fg_color= "blue", text= "show", border_color= "blue", text_color= "grey60", corner_radius= 15, command=lambda:self.showPassword(self.getCensor()))
        self.censorbox.grid(row= 0, column= 0, sticky= "e", padx= 10)
        
        self.copyButton = ctk.CTkButton(optFrame, fg_color= "#ade298", width=30, text= "copy", text_color= "#242424", corner_radius= 15, command=lambda:self.copyPassword(), hover_color="#63984e")
        self.copyButton.grid(row= 0, column= 1, sticky= "e", padx= 10)
        
        if self.__id != "1":
            self.deleteButton = ctk.CTkButton(optFrame, fg_color= "#f0738c", width=30, text= "delete", text_color= "#E2E2E2", corner_radius= 15, command=lambda:self.deletePassword(), hover_color="#c32a3c")
            self.deleteButton.grid(row= 0, column= 2, sticky= "e", padx= 10)
            
            self.editButton = ctk.CTkButton(optFrame, fg_color= "#7978dc", width=30, text= "edit", text_color= "#E2E2E2", corner_radius= 15, command=lambda:self.editPassword(), hover_color="#2a2fc3")
            self.editButton.grid(row= 0, column= 3, sticky= "e", padx= 10)
        else:
            self.deleteButton = ctk.CTkButton(optFrame, fg_color= "#f0738c", width=30, text= "delete Acc", text_color= "#E2E2E2", corner_radius= 15, command=lambda:self.deleteUser(), hover_color="#c32a3c")
            self.deleteButton.grid(row= 0, column= 2, sticky= "e", padx= 10)
            
            self.editButton = ctk.CTkButton(optFrame, fg_color= "#7978dc", width=30, text= "edit", text_color= "#E2E2E2", corner_radius= 15, command=lambda:self.editPassword(), hover_color="#2a2fc3")
            self.editButton.grid(row= 0, column= 3, sticky= "e", padx= 10)
            
        self.text2 = ctk.CTkLabel(self, text = f"Password: {password_text}", padx= 10, fg_color="grey30", pady = 5, anchor= "w")
        self.text2.grid(row = 2, column = 0, sticky= "we", columnspan= 1)

    def getCensor(self) -> bool:
        """
        Vor.: --
        Eff.: --
        Erg.: Gibt den Zustand der 'Censorbox' zurück
        """
        return self.censorbox.get()

    def showPassword(self, censorState: bool) -> None:
        """
        Vor.: Den Status der 'Censorbox'
        Eff.: Ändern der Variable 'password_text'
        Erg.: Änderung des Anzeigestatus des Passwortes
        """
        if censorState == False:
            password_text = "*" * len(self.password)
        else:
            password_text = self.password
        
        self.text2 = ctk.CTkLabel(self, text = f"Password: {password_text}", padx= 10, fg_color="grey30", pady = 5, anchor= "w")
        self.text2.grid(row = 2, column = 0, sticky= "we", columnspan= 1)
    
    def copyPassword(self) -> None:
        """
        Vor.: --
        Eff.: Clipboard-Data wird beschrieben
        Erg.: CLipboard enthält das Passwort
        """
        clip.copy(self.password)

    def deletePassword(self) -> None:
        """
        Vor.: --
        Eff.: Ein Passwortobjekt wird in der Datenbank gelöscht beim Benutzer: 'username'
        Erg.: Passwortkarte wird gelöscht
        """
        dbf.deletePasswordCard(DBMS, username, self.__id)
        passwordList = []
        userdata = dbf.readUserdata(DBMS, username)
        for i in range(len(userdata["password_cards"])):
            passwordList.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
        self.master.values = passwordList
        self.master.refresh()
        
    def editPassword(self) -> None:
        """
        Vor.: --
        Eff.: Die Werte des Passwortkartenobjektes werden in der Datenbank gespeichert
        Erg.: Passwortkarte wird geändert
        """
        new_username = ctk.CTkInputDialog(text="Edit Username", title="Edit Username?").get_input()
        new_password = ctk.CTkInputDialog(text="Edit Password", title="Edit Password?").get_input()
        if not new_username:
            new_username = self.username
        if not new_password:
            new_password = self.password

        if self.__id == "1":
            updateLogin = dbf.updateLogin(DBMS, username, new_username, new_password)
            if updateLogin == True:
                dbf.editPasswordCard(DBMS, username, self.__id, new_username, new_password)
                self.username = new_username
                self.password = new_password
            else:
                dbf.updateLogin(DBMS, username, username, self.password)
                mbox.showerror("Error", "Username already in use!")
        else:
            dbf.editPasswordCard(DBMS, username, self.__id, new_username, new_password)        
            self.username = new_username
            self.password = new_password
        self.text1.configure(text=f"Username: {self.username}")
        self.showPassword(self.getCensor())
    
    def deleteUser(self) -> None:
        """
        Vor.: --
        Eff.: Das Datentupel des Benutzers 'username' wird aus der Datenbannktabelle 'users' gelöscht
        Erg.: Der Account wird gelöscht
        """
        new_password = ctk.CTkInputDialog(text="Type 'Delete my LOCKER'", title="Do you realy want to delete your Account?").get_input()
        if new_password == "Delete my LOCKER":
            dbf.deleteUser(DBMS, username)
            sys.exit()    

class PasswordScroll(ctk.CTkScrollableFrame):
    def __init__(self, master, values: list[tuple]):
        """
        Vor.: Variablen: master, values
        Eff.: Eine Objekt der Klasse PasswordScroll wird gespeichert
        Erg.: Objekt der Klasse PasswordFrame mit den Attributen values und frames wird erstellt
        """  
        super().__init__(master)

        self.values = values
        self.frames = []

        self.grid_columnconfigure(0, weight= 1)
        self.grid_rowconfigure(len(self.values), weight = 1)

        for i, element in enumerate(self.values):
            card_id = element[0] 
            website = element[1]
            username = element[2]
            password = element[3]
            uncensor = False
            
            self.frame = PasswordFrame(self, card_id, website, username, password, uncensor)
            self.frame.grid(row = i, column= 0, sticky = "we")
            self.frames.append(self.frame)

    def refresh(self):
        """
        Vor.: --
        Eff.: Datenbankobjekte werden ausgelesen
        Erg.: Das 'PasswordScroll' wird mit den ausgelesenen Daten erneuert
        """
        for widget in self.winfo_children():
            widget.destroy()
            
        for i, element in enumerate(self.values):
            card_id = element[0] 
            website = element[1]
            username = element[2]
            password = element[3]
            uncensor = False

            self.frame = PasswordFrame(self, card_id, website, username, password, uncensor)
            self.frame.grid(row = i, column= 0, sticky = "we")

            self.frames.append(self.frame)
        for self.frame in self.frames:
            if self.frame.getCensor() == 1: 
                self.frame.configure(uncensor= True)

class Login(ctk.CTk):
    def __init__(self) -> None:
        """
        Vor.: Variablen: passwordList
        Eff.: Eine Objekt der Klasse GUI wird gespeichert
        Erg.: Objekt der Klasse GUI als grafische Benutzeroberfläche wird erstellt
        """
        super().__init__()
        self.action = "login"
        self.geometry("400x300")
        self.title("Password Manager")

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        
        self.loginForm = ctk.CTkFrame(self, corner_radius= 10, bg_color="#242424", fg_color="transparent")
        self.loginForm.grid(row= 0, column= 0, sticky= "news")
        
        self.loginLabel = ctk.CTkLabel(self.loginForm, text="Login", font=("Arial", 20), corner_radius= 10, bg_color="#242424", fg_color="#242424")
        self.loginLabel.pack(pady=20, padx=20)
        
        self.userInput = ctk.CTkEntry(self.loginForm, placeholder_text="Benutzername", width= 200, bg_color="#242424", fg_color="#242424")
        self.userInput.pack(pady=10, padx=20)
        
        self.passInput = ctk.CTkEntry(self.loginForm, placeholder_text="Passwort", width= 200, bg_color="#242424", fg_color="#242424", show="*")
        self.passInput.pack(pady=10, padx=20)
        
        self.menu = ctk.CTkFrame(self, height= 100, corner_radius= 10, fg_color="#121212")
        self.menu.grid(row= 1, column= 0, sticky= "ew")
        
        self.leaveButton = ctk.CTkButton(self.menu, text="Leave", fg_color="#f0738c", width= 100, corner_radius= 15, hover_color="#c32a3c", command=lambda:sys.exit())
        self.leaveButton.pack(side="right", padx= 10, pady= 10, fill="x", expand=True)
        
        self.loginButton = ctk.CTkButton(self.menu, text="Login", fg_color="#7978dc", width= 100, corner_radius= 15, hover_color="#2a2fc3", command=lambda:self.loginUser("login"))
        self.loginButton.pack(side="right", padx= 10, pady= 10, fill="x", expand=True)
        
        self.registerButton = ctk.CTkButton(self.menu, text="Register", fg_color="#78dc96", width= 100, corner_radius= 15, hover_color="#2ac33c", command=lambda:self.loginUser("register"))
        self.registerButton.pack(side="right", padx= 10, pady= 10, fill="x", expand=True)
    
    def loginUser(self, action: str) -> None:
        """
        Vor.: --
        Eff.: Login-Funktion wird aufgerufen
        Erg.: Login wird durchgeführt
        """
        global DBMS, username, password
        DBMS = dbf.connect_L0CKER_DB(r"backend/l0ck3rdb.duckdb")
        self.action = action
        username = self.userInput.get()
        password = self.passInput.get()
        
        if self.action == "login":
            passwordList = []
            login = dbf.L0CKin(DBMS, username, password)
            if login == True:
                userdata = dbf.readUserdata(DBMS, username)
                for i in range(len(userdata["password_cards"])):
                    passwordList.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
                mbox.showinfo("Login", f"Welcome back, {username}!\nlatest access: {userdata["latest_access"]}")
                ctk.set_appearance_mode("dark")
                ctk.set_default_color_theme("blue")
                app = GUI(passwordList)
                self.destroy()
                app.mainloop()
                
            else:
                mbox.showerror("Login", "Wrong username or password provided!")
        
        elif self.action == "register":
            passwordList = []
            login = dbf.R3gister(DBMS, username, password)
            if login == True:
                userdata = dbf.readUserdata(DBMS, username)
                for i in range(len(userdata["password_cards"])):
                    passwordList.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
                mbox.showinfo("Register", f"Welcome to miniL0CK3R, {username}!")
                ctk.set_appearance_mode("dark")
                ctk.set_default_color_theme("blue")
                app = GUI(passwordList)
                self.destroy()
                app.mainloop()
                
            else:
                mbox.showerror("Register", "Username already in use!")

            
class GUI(ctk.CTk):
    def __init__(self, passwordList: list) -> None:
        """
        Vor.: Variablen: passwordList
        Eff.: Eine Objekt der Klasse GUI wird gespeichert
        Erg.: Objekt der Klasse GUI als grafische Benutzeroberfläche wird erstellt
        """
        super().__init__()
        self.geometry("600x500")
        self.title("Password Manager")

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        
        self.password_scroll = PasswordScroll(self, passwordList)
        self.password_scroll.grid(row= 0, column= 0, sticky= "news")
        
        self.menu = ctk.CTkFrame(self, height= 100, corner_radius= 10, bg_color="#242424", fg_color="#242424")
        self.menu.grid(row= 1, column= 0, sticky= "ew")
        
        self.leaveButton = ctk.CTkButton(self.menu, text="Leave", fg_color="#f0738c", width= 100, corner_radius= 15, hover_color="#c32a3c", command=lambda:sys.exit())
        self.leaveButton.pack(side="right", padx= 10, pady= 10, fill="x", expand=True)
        
        self.addButton = ctk.CTkButton(self.menu, text="Add Password", fg_color="#7978dc", width= 100, corner_radius= 15, hover_color="#2a2fc3", command=lambda:self.addPassword())
        self.addButton.pack(side="right", padx= 10, pady= 10, fill="x", expand=True)
        
    def addPassword(self) -> None:
        """
        Vor.: --
        Eff.: Fügt ein Passwortobjekt in der Datenbank unter dem Benutzer hinzu
        Erg.: Ein weiteres Passwort
        """
        add_website = ctk.CTkInputDialog(text="Website", title="Add Password").get_input()
        add_username = ctk.CTkInputDialog(text="Username", title="Add Password").get_input()
        add_password = ctk.CTkInputDialog(text="Password", title="Add Password").get_input()
        
        if add_website and add_username and add_password:
            dbf.addPasswordCard(DBMS, username, add_website, add_username, add_password)
            passwordList = []
            userdata = dbf.readUserdata(DBMS, username)
            for i in range(len(userdata["password_cards"])):
                passwordList.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
            self.password_scroll.values = passwordList
            self.password_scroll.refresh()


def main():
    """
    Vor.: --
    Eff.: Diese Funktion wird beim Aufrufen dieser Datei ausgeführt
    Erg.: Das Hauptprogram
    """
    global DBMS, username
    running = True
    login = False
    passwordList = []
    wrongCount = 1
    username = ""
    password = ""
    DBMS = dbf.connect_L0CKER_DB(r"backend/l0ck3rdb.duckdb")
    print("Bulding miniL0CK3R...")
    print("Welcome to miniL0CK3R!\n")
    action = input("Choose an action ( login | register | exit ):\n")
    if action == "exit" or action not in ["login", "register"]:
        sys.exit()
    while running: 
        if login:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            app = GUI(passwordList)
            app.mainloop()
            running = False

        else:
            if action == "login":
                print("Login\n")
                username = input("Username: ")
                password = input("Password: ")
                login = dbf.L0CKin(DBMS, username, password)
                if login == True:
                    print(f"Welcome back, {username}!")
                    userdata = dbf.readUserdata(DBMS, username)
                    print(f"latest access: {userdata["latest_access"]}")
                    for i in range(len(userdata["password_cards"])):
                        passwordList.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
                else:
                    print(f"Wrong username or password provided!\nTry again ({3-wrongCount} remaining)")
                    wrongCount += 1
                    if wrongCount > 3:
                        print("Danger!!\nClosing DB")
                        sys.exit()
                            
            elif action == "register":
                print("Register\n")
                username = input("Username: ")
                password = input("Password: ")
                login = dbf.R3gister(DBMS, username, password)
                if login == True:
                    print(f"Welcome back, {username}!")
                    userdata = dbf.readUserdata(DBMS, username)
                    for i in range(len(userdata["password_cards"])):
                        passwordList.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
                    print(f"latest access: {userdata["latest_access"]}")
                else:
                    print(f"Sorry, username already in use!\n")

if __name__ == "__main__":
    login = Login()
    login.mainloop()
