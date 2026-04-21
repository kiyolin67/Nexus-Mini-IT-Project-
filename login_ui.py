import customtkinter as ctk

ctk.set_appearance_mode("light")#background colour
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("Login")

def handle_login():
    username = user_entry.get()
    password = pass_entry.get()

    if username == "" or password == "":
        status_label.configure(text="Please fill all fields", text_colour="red")
    elif username == "admin" and password == "1234": #lingesh please connect this to the user database later
        status_label.configure(text="Login succesfull", text_colour="green")
    else:
        status_label.configure(text="your provided credentials is invalid", text_colour="red")  


title = ctk.CTkLabel(app, text="Login page", font=("Arial", 20))#please double check if arial is good or should we change too different font
title.pack(pady=20)

user_entry = ctk.CTkEntry(app, placeholder_text = "Username")
user_entry.pack(pady=10)

pass_entry = ctk.CTkEntry(app, placeholder_text= "Password", show="*")
pass_entry.pack(pady=10)

login_button = ctk.CTkButton(app, text="Login", command=handle_login)
login_button.pack(pady=10)

status_label = ctk.CTkLabel(app, text="")
status_label.pack()

app.mainloop()


"""
things to add 
when inputting wrong credential clear only password keep username
password view toggler
open new window on success + display success/ failure window
maybe change colour after more discussion with team members blue/white is kinda boring
"""
