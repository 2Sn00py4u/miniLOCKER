import customtkinter as ctk
import tldextract
import backend.duck_functions as dbf
import sys
import pyperclip as clip


class PasswortFrame(ctk.CTkFrame):

    def __init__(self, master, id, website, username, password, uncensor):

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

        # row1: username

        self.text1 = ctk.CTkLabel(self, text = f"Username: {username}", padx=10, fg_color="grey30", pady = 5, anchor = "w")
        self.text1.grid(row = 1, column = 0, columnspan= 2 , sticky = "we")

        optFrame = ctk.CTkFrame(self, width=200, corner_radius=10, bg_color="grey20")
        optFrame.grid(row = 2, column = 1, sticky = "ew")
        
        #col2: censor checkbox

        self.censorbox = ctk.CTkCheckBox(optFrame, fg_color= "blue", text= "show", border_color= "blue", text_color= "grey60", corner_radius= 15, command=lambda:self.showPassword(self.getCensor()))
        self.censorbox.grid(row= 0, column= 0, sticky= "e", padx= 10)
        
        self.copyButton = ctk.CTkButton(optFrame, fg_color= "#ade298", width=30, text= "copy", text_color= "#242424", corner_radius= 15, command=lambda:self.copyPassword(), hover_color="#63984e")
        self.copyButton.grid(row= 0, column= 1, sticky= "e", padx= 10)
        
        if self.__id != "1":
            self.deleteButton = ctk.CTkButton(optFrame, fg_color= "#f0738c", width=30, text= "delete", text_color= "#C5C5C5", corner_radius= 15, command=lambda:self.deletePassword(), hover_color="#c32a3c")
            self.deleteButton.grid(row= 0, column= 2, sticky= "e", padx= 10)
            
            self.editButton = ctk.CTkButton(optFrame, fg_color= "#7978dc", width=30, text= "edit", text_color= "#C5C5C5", corner_radius= 15, command=lambda:self.editPassword(), hover_color="#2a2fc3")
            self.editButton.grid(row= 0, column= 3, sticky= "e", padx= 10)
        else:
            self.editButton = ctk.CTkButton(optFrame, fg_color= "#7978dc", width=30, text= "edit", text_color= "#C5C5C5", corner_radius= 15, command=lambda:self.editPassword(), hover_color="#2a2fc3")
            self.editButton.grid(row= 0, column= 2, sticky= "e", padx= 10)
            
        # col1: text
        self.text2 = ctk.CTkLabel(self, text = f"Password: {password_text}", padx= 10, fg_color="grey30", pady = 5, anchor= "w")
        self.text2.grid(row = 2, column = 0, sticky= "we", columnspan= 1)

    def getCensor(self) -> bool: 
        return self.censorbox.get()

    def showPassword(self, censorState: bool) -> None:
        if censorState == False:
            password_text = "*" * len(self.password)
        else:
            password_text = self.password
        
        self.text2 = ctk.CTkLabel(self, text = f"Password: {password_text}", padx= 10, fg_color="grey30", pady = 5, anchor= "w")
        self.text2.grid(row = 2, column = 0, sticky= "we", columnspan= 1)
    
    def copyPassword(self) -> None:
        clip.copy(self.password)

    def deletePassword(self) -> None:
        dbf.deletePasswordCard(DBMS, username, self.website)
        liste = []
        userdata = dbf.readUserdata(DBMS, username)
        for i in range(len(userdata["password_cards"])):
            liste.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
        self.master.values = liste
        self.master.refresh()
        
    def editPassword(self) -> None:
        new_username = ctk.CTkInputDialog(text="Edit Username", title="Edit Username?").get_input()
        new_password = ctk.CTkInputDialog(text="Edit Password", title="Edit Password?").get_input()
        if not new_username:
            new_username = self.username
        if not new_password:
            new_password = self.password
        #print(new_username, new_password)
        dbf.editPasswordCard(DBMS, username, self.__id, new_username, new_password)
        self.username = new_username
        self.password = new_password
        self.text1.configure(text=f"Username: {self.username}")
        self.showPassword(self.getCensor())
        

class PasswordScroll(ctk.CTkScrollableFrame):
    def __init__(self, master, values):
        
        # values = [(card_id, website, username, password), (...) ...]
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

            self.frame = PasswortFrame(self, card_id, website, username, password, uncensor)
            self.frame.grid(row = i, column= 0, sticky = "we")

            self.frames.append(self.frame)

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        for i, element in enumerate(self.values):
            card_id = element[0] 
            website = element[1]
            username = element[2]
            password = element[3]

            uncensor = False

            self.frame = PasswortFrame(self, card_id, website, username, password, uncensor)
            self.frame.grid(row = i, column= 0, sticky = "we")

            self.frames.append(self.frame)
        for self.frame in self.frames:
            if self.frame.getCensor() == 1: 
                self.frame.configure(uncensor= True)
            
            

#hauptklasse
class GUI(ctk.CTk):

    def __init__(self, liste) -> None:
        
        super().__init__()
        self.geometry("600x500")
        self.title("Password Manager")

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.test_scroll = PasswordScroll(self, liste)
        self.test_scroll.grid(row= 0, column= 0, sticky= "news")
    
    def test():
        print("test")

def main():
    global DBMS, username
    running = True
    login = False
    liste = []
    wrongCount = 1
    username = ""
    password = ""
    DBMS = dbf.connect_L0CKER_DB(r"backend/l0ck3rdb.duckdb")
    print("Bulding miniL0CK3R...")
    print("Welcome to miniL0CK3R")
    action = input("Choose an action ( login | register | exit ):\n")
    if action == "exit" or action not in ["login", "register"]:
        sys.exit()
    while running: 
        if login:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            app = GUI(liste)
            app.mainloop()
            running = False

        
        else:
            if action == "login":
                print("Login\n")
                username = input("Benutzername: ")
                password = input("Passwort: ")
                login = dbf.L0CKin(DBMS, username, password)
                if login == True:
                    print(f"Welcome back, {username}!")
                    userdata = dbf.readUserdata(DBMS, username)
                    print(f"latest access: {userdata["latest_access"]}")
                    for i in range(len(userdata["password_cards"])):
                        liste.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
                else:
                    print(f"Wrong username or password provided!\nTry again ({3-wrongCount} remaining)")
                    wrongCount += 1
                    if wrongCount > 3:
                        print("Danger!!\nClosing DB")
                        sys.exit()
                            
            elif action == "register":
                print("Register\n")
                username = input("Benutzername: ")
                password = input("Passwort: ")
                login = dbf.R3gister(DBMS, username, password)
                if login == True:
                    print(f"Welcome back, {username}!")
                    userdata = dbf.readUserdata(DBMS, username)
                    for i in range(len(userdata["password_cards"])):
                        liste.append((userdata["password_cards"][i]["card_id"], userdata["password_cards"][i]["website"], userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
                    print(f"latest access: {userdata["latest_access"]}")
                else:
                    print(f"Sorry, username already in use!\n")

if __name__ == "__main__":
    main()
