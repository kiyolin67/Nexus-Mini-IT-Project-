import customtkinter as ctk

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, success_callback):
        super().__init__(parent, fg_color="#0A0F1D") # Deep Midnight Background

        self.success_callback = success_callback
        self.password_visible = False
        self.users = {"admin": "1234"}

        # Title
        ctk.CTkLabel(
            self, 
            text="NEXUS PORTAL", 
            font=("Arial", 32, "bold"), 
            text_color="#00F0FF" # Electric Teal Accent
        ).pack(pady=(60, 5))
        
        ctk.CTkLabel(
            self, 
            text="Academic Management System", 
            font=("Arial", 14), 
            text_color="#8A99AD" # Muted Slate Blue
        ).pack(pady=(0, 30))

        # Username Entry
        self.user_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Username", 
            width=260, 
            height=40,
            fg_color="#131C32",
            border_color="#1F2E54",
            text_color="#FFFFFF",
            placeholder_text_color="#526484"
        )
        self.user_entry.pack(pady=10)

        # Password Entry Area
        self.pass_container = ctk.CTkFrame(self, fg_color="transparent")
        self.pass_container.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(
            self.pass_container, 
            placeholder_text="Password", 
            show="*", 
            width=210, 
            height=40,
            fg_color="#131C32",
            border_color="#1F2E54",
            text_color="#FFFFFF",
            placeholder_text_color="#526484"
        )
        self.pass_entry.pack(side="left")

        self.show_btn = ctk.CTkButton(
            self.pass_container, 
            text="👁", 
            width=45, 
            height=40,
            fg_color="#1F2E54", 
            hover_color="#2D437A",
            text_color="#00F0FF",
            command=self.toggle_password
        )
        self.show_btn.pack(side="left", padx=5)

        # Login Button
        self.login_btn = ctk.CTkButton(
            self, 
            text="ACCESS SYSTEM", 
            font=("Arial", 13, "bold"),
            width=260, 
            height=45,
            fg_color="#00F0FF",
            hover_color="#00C8D6",
            text_color="#0A0F1D", # Contrast dark text on bright button
            command=self.login
        )
        self.login_btn.pack(pady=(25, 10))

        # Create User Button
        self.signup_btn = ctk.CTkButton(
            self, 
            text="Register New Account", 
            width=260, 
            height=40,
            fg_color="transparent", 
            border_width=1,
            border_color="#1F2E54",
            text_color="#8A99AD",
            hover_color="#131C32",
            command=self.create_user
        )
        self.signup_btn.pack(pady=10)

        # Status Label
        self.status = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status.pack(pady=20)

    def toggle_password(self):
        if self.password_visible:
            self.pass_entry.configure(show="*")
            self.show_btn.configure(text="👁")
            self.password_visible = False
        else:
            self.pass_entry.configure(show="")
            self.show_btn.configure(text="✕")
            self.password_visible = True

    def login(self):
        user = self.user_entry.get()
        pw = self.pass_entry.get()
        if user in self.users and self.users[user] == pw:
            self.status.configure(text="Access Granted", text_color="#00FF66") # Success Green
            self.success_callback()
        else:
            self.status.configure(text="Invalid Security Credentials", text_color="#FF3366") # Alert Red

    def create_user(self):
        user = self.user_entry.get()
        pw = self.pass_entry.get()
        if user and pw:
            if user not in self.users:
                self.users[user] = pw
                self.status.configure(text=f"User registered successfully.", text_color="#00FF66")
            else:
                self.status.configure(text="Identity registry already exists.", text_color="#FFCC00") # Warning Amber
        else:
            self.status.configure(text="All clearance fields required.", text_color="#FF3366")