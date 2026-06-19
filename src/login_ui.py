import customtkinter as ctk
from database import set_current_user
from main import NexusApp 

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")
password_visible = False

app = ctk.CTk()
app.geometry("400x420") 
app.title("Nexus - Secure Login")

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
    elif username == "admin" and password == "1234": 
        set_current_user(username)
        status_label.configure(text="Login successful!", text_color="green")
        
        app.destroy() 
        
        print(f"Launching Nexus OS for {username}...")
        main_dashboard = NexusApp()
        main_dashboard.mainloop()
        
    else:
        status_label.configure(text="Your provided credentials are invalid", text_color="red")  
        pass_entry.delete(0, 'end') 

def show_login():
    clear_window()

    global user_entry, pass_entry, status_label, toggle_button

    title = ctk.CTkLabel(app, text="Nexus Portal", font=("Helvetica", 24, "bold"), text_color="#3498db")
    title.pack(pady=20)

    user_entry = ctk.CTkEntry(app, placeholder_text="Username", width=200)
    user_entry.pack(pady=10)

    pass_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=200)
    pass_entry.pack(pady=10)

    toggle_button = ctk.CTkButton(app, text="Show Password", width=150, fg_color="transparent", border_width=1, command=toggle_password)
    toggle_button.pack(pady=5)

    login_button = ctk.CTkButton(app, text="Login", width=200, fg_color="#2ecc71", hover_color="#27ae60", font=("Arial", 14, "bold"), command=handle_login)
    login_button.pack(pady=15)

    status_label = ctk.CTkLabel(app, text="")
    status_label.pack()

    register_button = ctk.CTkButton(app, text="Create Account", fg_color="transparent", hover_color="#2c3e50", command=show_register)
    register_button.pack(pady=10)

def show_register():
    clear_window()

    title = ctk.CTkLabel(app, text="Register", font=("Helvetica", 20, "bold"))
    title.pack(pady=20)

    user_entry_reg = ctk.CTkEntry(app, placeholder_text="Username", width=200)
    user_entry_reg.pack(pady=10)

    pass_entry_reg = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=200)
    pass_entry_reg.pack(pady=10)

    confirm_entry = ctk.CTkEntry(app, placeholder_text="Confirm Password", show="*", width=200)
    confirm_entry.pack(pady=10)

    status_label_reg = ctk.CTkLabel(app, text="")
    status_label_reg.pack()

    def register_user():
        u = user_entry_reg.get()
        p = pass_entry_reg.get()
        c = confirm_entry.get()

        if u == "" or p == "" or c == "":
            status_label_reg.configure(text="Fill all fields", text_color="red")
        elif p != c:
            status_label_reg.configure(text="Passwords do not match", text_color="red")
        else:
            status_label_reg.configure(text="Registered successfully", text_color="green")

    register_btn = ctk.CTkButton(app, text="Register", width=200, command=register_user)
    register_btn.pack(pady=10)

    back_btn = ctk.CTkButton(app, text="Back to Login", fg_color="transparent", command=show_login)
    back_btn.pack(pady=5)

show_login()
app.mainloop()