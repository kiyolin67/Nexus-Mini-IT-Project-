import customtkinter as ctk
import database as db
from main import NexusApp 
from admin_page import AdminDashboard

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

# --- STUDY PALETTE THEME ---
# Primary Accent (Slate/Nordic Blue): #5e81ac
# Action Button (Calming Sage Green): #4f6f52
# Action Hover (Darker Forest Sage):  #3a533c
# Muted Text/Buttons (Soft Charcoal): #3b4252

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

password_visible = False

app = ctk.CTk()
app.geometry("400x420") 
app.title("Nexus Study Portal - Secure Login")

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
        status_label.configure(text="Please fill all fields", text_color="#bf616a") # Soft red
    else:
        if db.is_admin(username, password):
            db.set_current_user("ADMIN")
            app.quit()
        elif db.user_exists(username, password):
            db.set_current_user(username)
            status_label.configure(text="Login successful!", text_color="#a3be8c") # Soft green
            app.quit()
        else:
            status_label.configure(text="Your provided credentials are invalid", text_color="#bf616a")
            pass_entry.delete(0, 'end')
def show_login():
    clear_window()

    global user_entry, pass_entry, status_label, toggle_button

    # Updated Title Color to soft slate blue
    title = ctk.CTkLabel(app, text="Nexus Portal", font=("Helvetica", 24, "bold"), text_color="#5e81ac")
    title.pack(pady=20)

    user_entry = ctk.CTkEntry(app, placeholder_text="Username", width=200)
    user_entry.pack(pady=10)

    pass_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=200)
    pass_entry.pack(pady=10)

    # Secondary toggle button matching theme
    toggle_button = ctk.CTkButton(app, text="Show Password", width=150, fg_color="transparent", border_width=1, border_color="#5e81ac", text_color="#5e81ac", command=toggle_password)
    toggle_button.pack(pady=5)

    # Login Button changed to Calming Sage Green
    login_button = ctk.CTkButton(app, text="Login", width=200, fg_color="#4f6f52", hover_color="#3a533c", font=("Arial", 14, "bold"), command=handle_login)
    login_button.pack(pady=15)

    status_label = ctk.CTkLabel(app, text="")
    status_label.pack()

    # Muted hover for secondary register option
    register_button = ctk.CTkButton(app, text="Create Account", fg_color="transparent", hover_color="#3b4252", text_color="#8892b0", command=show_register)
    register_button.pack(pady=10)

def show_register():
    clear_window()

    # Main container frame (creates a nice "card" effect for the form)
    card_frame = ctk.CTkFrame(app, fg_color="#2e3440", corner_radius=15)
    card_frame.pack(pady=30, padx=30, fill="both", expand=True)

    # Header section
    title = ctk.CTkLabel(
        card_frame, 
        text="Create Account", 
        font=("Helvetica", 22, "bold"), 
        text_color="#5e81ac" # Nordic Blue
    )
    title.pack(pady=(25, 5))

    subtitle = ctk.CTkLabel(
        card_frame, 
        text="Join the Nexus study portal", 
        font=("Helvetica", 12), 
        text_color="#8892b0" # Muted Slate
    )
    subtitle.pack(pady=(0, 15))

    # Input Fields with custom border styling
    user_entry_reg = ctk.CTkEntry(
        card_frame, 
        placeholder_text="Choose Username", 
        width=240,
        height=35,
        border_color="#434c5e",
        fg_color="#3b4252"
    )
    user_entry_reg.pack(pady=8)

    pass_entry_reg = ctk.CTkEntry(
        card_frame, 
        placeholder_text="Create Password", 
        show="*", 
        width=240,
        height=35,
        border_color="#434c5e",
        fg_color="#3b4252"
    )
    pass_entry_reg.pack(pady=8)

    confirm_entry = ctk.CTkEntry(
        card_frame, 
        placeholder_text="Confirm Password", 
        show="*", 
        width=240,
        height=35,
        border_color="#434c5e",
        fg_color="#3b4252"
    )
    confirm_entry.pack(pady=8)

    # Contextual status/error label space
    status_label_reg = ctk.CTkLabel(card_frame, text="", font=("Helvetica", 12))
    status_label_reg.pack(pady=2)

    # Core Register Logic (retaining original database hooks)
    def register_user():
        u = user_entry_reg.get()
        p = pass_entry_reg.get()
        c = confirm_entry.get()

        if u == "" or p == "" or c == "":
            status_label_reg.configure(text="Please fill all fields", text_color="#bf616a") # Soft red
        elif p != c:
            status_label_reg.configure(text="Passwords do not match", text_color="#bf616a")
        else:
            success = db.save_user(u, p)
            if success:
                status_label_reg.configure(text="Account created successfully!", text_color="#a3be8c") # Soft green
                user_entry_reg.delete(0, 'end')
                pass_entry_reg.delete(0, 'end')
                confirm_entry.delete(0, 'end')
            else:
                status_label_reg.configure(text="Username already exists", text_color="#bf616a")
                
    # Primary Action Button (Sage Green)
    register_btn = ctk.CTkButton(
        card_frame, 
        text="Register", 
        width=240, 
        height=40,
        fg_color="#4f6f52", 
        hover_color="#3a533c", 
        font=("Helvetica", 14, "bold"), 
        command=register_user
    )
    register_btn.pack(pady=(15, 5))

    # Secondary Navigation Button
    back_btn = ctk.CTkButton(
        card_frame, 
        text="← Back to Login", 
        fg_color="transparent", 
        hover_color="#3b4252", 
        text_color="#8892b0", 
        font=("Helvetica", 12),
        command=show_login
    )
    back_btn.pack(pady=(0, 15))


def show_login():
    clear_window()

    global user_entry, pass_entry, status_label, toggle_button

    # Updated Title Color to soft slate blue
    title = ctk.CTkLabel(app, text="Nexus Portal", font=("Helvetica", 24, "bold"), text_color="#5e81ac")
    title.pack(pady=20)

    user_entry = ctk.CTkEntry(app, placeholder_text="Username", width=200)
    user_entry.pack(pady=10)

    pass_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*", width=200)
    pass_entry.pack(pady=10)

    # Secondary toggle button matching theme
    toggle_button = ctk.CTkButton(app, text="Show Password", width=150, fg_color="transparent", border_width=1, border_color="#5e81ac", text_color="#5e81ac", command=toggle_password)
    toggle_button.pack(pady=5)

    # Login Button changed to Calming Sage Green
    login_button = ctk.CTkButton(app, text="Login", width=200, fg_color="#4f6f52", hover_color="#3a533c", font=("Arial", 14, "bold"), command=handle_login)
    login_button.pack(pady=15)

    status_label = ctk.CTkLabel(app, text="")
    status_label.pack()

    # Muted hover for secondary register option
    register_button = ctk.CTkButton(app, text="Create Account", fg_color="transparent", hover_color="#3b4252", text_color="#8892b0", command=show_register)
    register_button.pack(pady=10)

def show_register():
    clear_window()

    title = ctk.CTkLabel(app, text="Register Account", font=("Helvetica", 20, "bold"), text_color="#5e81ac")
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
        status_label_reg.configure(text="Fill all fields", text_color="#bf616a")
    elif p != c:
        status_label_reg.configure(text="Passwords do not match", text_color="#bf616a")
    else:
        success = db.save_user(u, p)
        if success:
            status_label_reg.configure(text="Account created successfully", text_color="#a3be8c")
            user_entry_reg.delete(0, 'end')
            pass_entry_reg.delete(0, 'end')
            confirm_entry.delete(0, 'end')
        else:
            status_label_reg.configure(text="Username already exists", text_color="#bf616a")
                
    # Register buttons formatted to match focus theme
    register_btn = ctk.CTkButton(app, text="Register", width=200, fg_color="#4f6f52", hover_color="#3a533c", font=("Arial", 14, "bold"), command=register_user)
    register_btn.pack(pady=10)

    back_btn = ctk.CTkButton(app, text="Back to Login", fg_color="transparent", hover_color="#3b4252", text_color="#8892b0", command=show_login)
    back_btn.pack(pady=5)
show_login()
app.mainloop()
app.destroy()

# Post-Login Handover
if db.CURRENT_USER == "ADMIN":
    print("Welcome, Admin!")
    admin_dashboard = AdminDashboard()
    admin_dashboard.mainloop()
elif db.CURRENT_USER is not None: 
    print(f"Welcome, {db.CURRENT_USER}!")
    main_dashboard = NexusApp()
    main_dashboard.mainloop()