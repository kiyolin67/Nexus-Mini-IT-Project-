import customtkinter as ctk
from database import set_current_user

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

ctk.set_appearance_mode("light")#background colour
ctk.set_default_color_theme("blue")

password_visible = False

app = ctk.CTk()
app.geometry("400x300")
app.title("Login")

def toggle_password():
    global password_visible

    if password_visible:
        pass_entry.configure(show="*")
        toggle_button.configure(text="Show Password")
        password_visible = False
    else:
        pass_entry.configure(show="")
        toggle_button.configure(text="Hide Password")
        password_visible = True

def handle_login():
    username = user_entry.get()
    password = pass_entry.get()

    if username == "" or password == "":
        status_label.configure(text="Please fill all fields", text_color="red")
    elif username == "admin" and password == "1234": #samuel please connect this to the user database later
        status_label.configure(text="Login succesfull", text_color="green")
    else:
        status_label.configure(text="your provided credentials is invalid", text_color="red")  

def show_login():
    clear_window()

    global user_entry, pass_entry, status_label, toggle_button

    title = ctk.CTkLabel(app, text="Login page", font=("Arial", 20))#please double check if arial is good or should we change too different font
    title.pack(pady=20)

    user_entry = ctk.CTkEntry(app, placeholder_text = "Username")
    user_entry.pack(pady=10)

    pass_entry = ctk.CTkEntry(app, placeholder_text= "Password", show="*")
    pass_entry.pack(pady=10)

    toggle_button = ctk.CTkButton(app, text="Show Password", command=toggle_password)
    toggle_button.pack(pady=5)

    login_button = ctk.CTkButton(app, text="Login", command=handle_login)
    login_button.pack(pady=10)

    status_label = ctk.CTkLabel(app, text="")
    status_label.pack()

    register_button = ctk.CTkButton(app, text="Create Account", command=show_register)
    register_button.pack(pady=5)




def show_register():
    clear_window()

    title = ctk.CTkLabel(app, text="Register", font=("Arial", 20))
    title.pack(pady=20)

    user_entry = ctk.CTkEntry(app, placeholder_text="Username")
    user_entry.pack(pady=10)

    pass_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*")
    pass_entry.pack(pady=10)

    confirm_entry = ctk.CTkEntry(app, placeholder_text="Confirm Password", show="*")
    confirm_entry.pack(pady=10)

    status_label = ctk.CTkLabel(app, text="")
    status_label.pack()

    def register_user():
        u = user_entry.get()
        p = pass_entry.get()
        c = confirm_entry.get()

        if u == "" or p == "" or c == "":
            status_label.configure(text="Fill all fields", text_color="red")
        elif p != c:
            status_label.configure(text="Passwords do not match", text_color="red")
        else:
            status_label.configure(text="Registered successfully", text_color="green")

    register_btn = ctk.CTkButton(app, text="Register", command=register_user)
    register_btn.pack(pady=10)

    back_btn = ctk.CTkButton(app, text="Back to Login", command=show_login)
    back_btn.pack(pady=5)


show_login()
app.mainloop()


"""
things to add
make 3 admin accounts
desktop based website
once samuel done created database have to start working on interface
interface maybe need to change colour theme

(lingesh)
make sure to seperate the part we explain from the api 
dont emphasis on the ai part unless its started 

bila presentation 
(sql will be stored in windows) sql is querry (which one is private which one foreign)

when inputting wrong credential clear only password keep username
open new window on success + display success/ failure window
maybe change colour after more discussion with team members blue/white is kinda boring


"""
