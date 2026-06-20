import customtkinter as ctk
import database as db

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("500x700")

        ctk.CTkLabel(self, text="Admin Dashboard", font=("Helvetica", 28, "bold"), text_color="#3498db").pack(pady=20)
        ctk.CTkLabel(self, text="Welcome, Admin!", font=("Helvetica", 18), text_color="#2ecc71").pack(pady=10)

        # Search Bar 
        self.search_var = ctk.StringVar(master=self)
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search users...",
            width=400,
            height=40,
            font=("Helvetica", 14),
            textvariable=self.search_var
        )
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.filter_users)
        
        self.user_list_frame = ctk.CTkScrollableFrame(self, width=400, height=400, fg_color="#ecf0f1", corner_radius=10)
        self.user_list_frame.pack(pady=10)

        self.all_users = db.get_all_users()
        self.populate_list(self.all_users)

    def filter_users(self, event):
        search_query = self.search_var.get().lower()
        filtered_data = [user for user in self.all_users if search_query in user[0].lower()]
        self.populate_list(filtered_data)
    
    def populate_list(self, user_data):
        for widget in self.user_list_frame.winfo_children():
            widget.destroy()
        
        if not user_data:
            ctk.CTkLabel(self.user_list_frame, text="No users found.", font=("Helvetica", 14), text_color="#e74c3c").pack(pady=30)
        else:
            for user in user_data:
                username = user[0]
            
                card = ctk.CTkFrame(self.user_list_frame, fg_color="#2b2b2b", corner_radius=5)
                card.pack(fill="x", pady=5, padx=10)
                
                ctk.CTkLabel(card, text=f"👤 {username}", font=("Helvetica", 16, "bold"), text_color="#3498db").pack(side="left", padx=15, pady=15)
                ctk.CTkLabel(card, text="[ Encrypted ]", text_color="gray").pack(side="right", padx=15, pady=15)