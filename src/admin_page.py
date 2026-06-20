import customtkinter as ctk
import database as db

class AdminDashboard(ctk.CTkFrame):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")

        ctk.CTkLabel(self, text="Admin Dashboard", font=("Helvetica", 28, "bold"), text_color="#3498db").pack(pady=20)
        ctk.CTkLabel(self, text="Welcome, Admin!", font=("Helvetica", 18), text_color="#2ecc71").pack(pady=10)

        self.user_listbox = ctk.CTkListbox(self, width=400, height=200, fg_color="#ecf0f1", text_color="#2c3e50")
        self.user_listbox.pack(pady=10)

        users = db.get_all_users()

        if not users:
            ctk.CTkLabel(self, text="No users found.", font=("Helvetica", 16), text_color="red").pack(pady=10)
        else:
            for user in users:
                username = user[0]

                # CARD

                card = ctk.CTkFrame(self, width=400, height=50, fg_color="#bdc3c7", corner_radius=10)
                card.pack(fill="x", padx=20, pady=5)

                ctk.CTkLabel(card, text=username, font=("Helvetica", 16, "bold"), text_color="#2c3e50").pack(side="left", padx=10, pady=10)
                ctk.CTkLabel(card, text="Encrypted", font=("Helvetica", 12), text_color="#27ae60").pack(side="right", padx=10, pady=10)

