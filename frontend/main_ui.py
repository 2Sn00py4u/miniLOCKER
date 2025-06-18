import customtkinter
import tldextract

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

        self.censorbox = customtkinter.CTkCheckBox(self, fg_color= "purple", text= "show", border_color= "purple", text_color= "grey60", corner_radius= 15)
        self.censorbox.grid(row= 2, column= 1, sticky= "w")

        # col1: text
        self.text2 = customtkinter.CTkLabel(self, text = f"Password: {password_text}", padx= 10, fg_color="grey30", pady = 5, anchor= "w")
        self.text2.grid(row = 2, column = 0, sticky= "we", columnspan= 1)

    def get(self): 

        return self.censorbox.get()

        

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

        

        
#list for testing purpose 
       
liste = [("https://pypi.org/project/tldextract/", "admin", "admin"),
         ("https://customtkinter.tomschimansky.com/documentation/widgets/textbox", "username", "user"),
         ("https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse", "peter", "baum"),
         ("google.com", "google_ceo", "i_like_money")]


#Aufruf der App
app = GUI(liste)
app.mainloop()