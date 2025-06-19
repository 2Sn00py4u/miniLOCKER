import customtkinter
import tldextract
import backend.duck_functions as dbf
import sys


class PasswortFrame(customtkinter.CTkFrame):

    def __init__(self, master, website, username, password, uncensor):

        super().__init__(master)

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

        self.title = customtkinter.CTkLabel(self, text = domain.top_domain_under_public_suffix, corner_radius = 10, fg_color = "purple", pady= 10, padx = 10 )
        self.title.grid(row = 0, column = 0, columnspan= 2, sticky = "ew")

        # row1: username

        self.text1 = customtkinter.CTkLabel(self, text = f"Username: {username}", padx=10, fg_color="grey30", pady = 5, anchor = "w")
        self.text1.grid(row = 1, column = 0, columnspan= 2 , sticky = "we")

        # row2: password

        #col2: censor checkbox

        self.censorbox = customtkinter.CTkCheckBox(self, fg_color= "purple", text= "show", border_color= "purple", text_color= "grey60", corner_radius= 15, command=lambda:self.showPassword(self.getConsor()))
        self.censorbox.grid(row= 2, column= 1, sticky= "w")

        # col1: text
        self.text2 = customtkinter.CTkLabel(self, text = f"Password: {password_text}", padx= 10, fg_color="grey30", pady = 5, anchor= "w")
        self.text2.grid(row = 2, column = 0, sticky= "we", columnspan= 1)

    def getConsor(self) -> bool: 
        return self.censorbox.get()

    def showPassword(self, censorState: bool) -> None:
        if censorState == False:
            password_text = "*" * len(self.password)
        else:
            password_text = self.password
        
        self.text2 = customtkinter.CTkLabel(self, text = f"Password: {password_text}", padx= 10, fg_color="grey30", pady = 5, anchor= "w")
        self.text2.grid(row = 2, column = 0, sticky= "we", columnspan= 1)
    
        

class PasswordScroll(customtkinter.CTkScrollableFrame):

    def __init__(self, master, values):
        
        # values = [(website, username, password), (...) ...]
        super().__init__(master)

        self.values = values
        self.frames = []

        self.grid_columnconfigure(0, weight= 1)
        self.grid_rowconfigure(len(self.values), weight = 1)


        for i, element in enumerate(self.values):

            website = element[0]
            username = element[1]
            password = element[2]

            uncensor = False

            self.frame = PasswortFrame(self, website, username, password, uncensor)
            self.frame.grid(row = i, column= 0, sticky = "we")

            self.frames.append(self.frame)

    def refresh(self):
        print("refresh")
        for self.frame in self.frames:

            if self.frame.get() == 1: 

                self.frame.configure(uncensor= True)
            
            

#hauptklasse
class GUI(customtkinter.CTk):

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
            #list for testing purpose 
            #liste = [("https://pypi.org/project/tldextract/", "admin", "admin"),
            #        ("https://customtkinter.tomschimansky.com/documentation/widgets/textbox", "username", "user"),
            #        ("https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse", "peter", "baum"),
            #        ("google.com", "google_ceo", "i_like_money")]

            #Aufruf der App
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
                        liste.append((f'www.{userdata["password_cards"][i]["card_title"]}.com', userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
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
                        liste.append((f'www.{userdata["password_cards"][i]["card_title"]}.com', userdata["password_cards"][i]["email"], userdata["password_cards"][i]["password"]))
                    print(f"latest access: {userdata["latest_access"]}")
                else:
                    print(f"Sorry, username already in use!\n")

if __name__ == "__main__":
    main()
