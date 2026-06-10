import customtkinter as ctk
import tkinter as tk

class RPGDashboard(ctk.CTkFrame):
    def __init__(self, master, daily_mins_studied, daily_goal, total_xp, **kwargs):
        super().__init__(master, fg_color="#2b2b2b", corner_radius=15, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        
        self.popup_window = None # Keep track of  popup

        # ==========================================
        # 1. THE DAILY FOCUS RING
        # ==========================================
        self.ring_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.ring_frame.grid(row=0, column=0, padx=20, pady=20)

        ctk.CTkLabel(self.ring_frame, text="Today's Focus", font=("Helvetica", 14, "bold"), text_color="gray").pack(pady=(0, 10))

        self.canvas_size = 140
        self.canvas = tk.Canvas(self.ring_frame, width=self.canvas_size, height=self.canvas_size, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack()

        # Math to calculate ring fill percentage
        fill_percentage = min(daily_mins_studied / daily_goal, 1.0)
        degrees = fill_percentage * 359.9  

        # Draw Background Ring (Dark Grey)
        self.canvas.create_arc(10, 10, self.canvas_size-10, self.canvas_size-10, start=0, extent=359.9, style="arc", outline="#3b3b3b", width=12)
        
        # Draw Foreground Ring (Neon Blue)
        ring_color = "#3498db" if fill_percentage < 1.0 else "#2ecc71" 
        self.canvas.create_arc(10, 10, self.canvas_size-10, self.canvas_size-10, start=90, extent=-degrees, style="arc", outline=ring_color, width=12)

        # Text in the middle of the ring
        self.canvas.create_text(self.canvas_size/2, self.canvas_size/2 - 10, text=f"{daily_mins_studied}m", fill="white", font=("Helvetica", 20, "bold"))
        self.canvas.create_text(self.canvas_size/2, self.canvas_size/2 + 15, text=f"/ {daily_goal}m goal", fill="gray", font=("Helvetica", 10))

        # ==========================================
        # 2. THE RPG PROGRESSION SYSTEM
        # ==========================================
        self.rpg_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.rpg_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        # XP Math: Every 1000 XP is a level
        current_level = (total_xp // 1000) + 1
        xp_into_level = total_xp % 1000
        xp_percentage = xp_into_level / 1000.0

        # Titles based on Level
        titles = ["Novice", "Initiate", "Adept", "Scholar", "Master", "Archmage"]
        title_index = min(current_level - 1, len(titles) - 1)
        current_title = titles[title_index]

        # Rank Header
        header_frame = ctk.CTkFrame(self.rpg_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(header_frame, text=f"Level {current_level}: {current_title}", font=("Helvetica", 24, "bold"), text_color="#f1c40f").pack(side="left")
        
        # --- THE NEW INFO ICON BUTTON ---
        self.info_btn = ctk.CTkButton(header_frame, text="❓", width=30, height=30, fg_color="transparent", hover_color="#444444", font=("Helvetica", 16), command=self.show_info_popup)
        self.info_btn.pack(side="left", padx=10)

        ctk.CTkLabel(header_frame, text=f"Total XP: {total_xp}", font=("Helvetica", 26, "bold"), text_color="green").pack(side="right", pady=5)

        # XP Progress Bar
        self.xp_bar = ctk.CTkProgressBar(self.rpg_frame, height=20, fg_color="#1e1e1e", progress_color="#f1c40f")
        self.xp_bar.pack(fill="x", pady=10)
        self.xp_bar.set(xp_percentage)

        ctk.CTkLabel(self.rpg_frame, text=f"{xp_into_level} / 1000 XP to next level", font=("Helvetica", 12), text_color="gray").pack(anchor="w")

    # ==========================================
    # 3. THE POPUP LOGIC
    # ==========================================
    def show_info_popup(self):
        # Prevent the user from spam-clicking and opening 50 windows 
        if self.popup_window is not None and self.popup_window.winfo_exists():
            self.popup_window.focus()
            return

        self.popup_window = ctk.CTkToplevel(self)
        self.popup_window.title("Dashboard Guide")
        self.popup_window.geometry("350x280")
        self.popup_window.configure(fg_color="#1e1e1e")
        
        # Forces the popup to stay on top of the main app
        self.popup_window.attributes("-topmost", True) 

        ctk.CTkLabel(self.popup_window, text="How Progression Works", font=("Helvetica", 20, "bold"), text_color="#3498db").pack(pady=(20, 10))

        rules_text = (
            "🎯 The Focus Ring\n"
            "Set a daily goal and track your active minutes. "
            "Close the ring to maintain your study consistency!\n\n"
            "⚔️ RPG Leveling\n"
            "• Every 1 minute studied = 10 XP\n"
            "• Every 1,000 XP = 1 Level Up\n"
            "• Reach higher levels to unlock advanced Scholar Titles."
        )

        ctk.CTkLabel(self.popup_window, text=rules_text, font=("Helvetica", 14), justify="left", wraplength=300).pack(pady=10, padx=20)
        
        ctk.CTkButton(self.popup_window, text="Got it!", fg_color="#2ecc71", hover_color="#27ae60", command=self.popup_window.destroy).pack(pady=(10, 20))