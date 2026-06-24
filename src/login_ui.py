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