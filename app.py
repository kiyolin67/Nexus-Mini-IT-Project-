import customtkinter as ctk
from login_page import LoginPage
from main_page import MainPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Initialize but don't pack yet
        self.main_page = MainPage(self.container)
        self.login_page = LoginPage(self.container, self.show_main)

        # Start with ONLY login
        self.show_login()

    def show_login(self):
        self.main_page.pack_forget()
        self.login_page.pack(fill="both", expand=True)

    def show_main(self):
        self.login_page.pack_forget()
        self.main_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()