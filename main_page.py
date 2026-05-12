import customtkinter as ctk

class MainPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure Grid: 2 Columns, 2 Rows
        # Column 0: Sidebar | Column 1: Content
        # Row 0: Top half (Cards) | Row 1: Bottom half (Graph)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1) # Top half
        self.grid_rowconfigure(1, weight=1) # Bottom half

        # --- 1. SIDEBAR (Left) ---
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(self.sidebar, text="Manage", font=("Arial", 20, "bold")).pack(pady=20)
        self.subject_input = ctk.CTkEntry(self.sidebar, placeholder_text="Subject Name")
        self.subject_input.pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Add Subject", command=self.add_subject).pack(pady=10)

        # --- 2. TOP RIGHT (Subject Cards) ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Study Sessions")
        self.scroll_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # --- 3. BOTTOM RIGHT (Graph Area) ---
        self.graph_frame = ctk.CTkFrame(self, fg_color="gray20")
        self.graph_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(self.graph_frame, text="Mastery Score Graph", font=("Arial", 16)).pack(pady=10)
        
        # Placeholder for the actual graph (Canvas or Matplotlib)
        self.graph_canvas = ctk.CTkFrame(self.graph_frame, fg_color="black", height=200)
        self.graph_canvas.pack(fill="both", expand=True, padx=20, pady=10)

        # --- 4. CHAT BOT AREA (Overlaid Bottom Right) ---
        # We use a separate frame that sits on top of the graph area
        self.chat_box = ctk.CTkFrame(self, width=250, height=150, border_width=2, border_color="cyan")
        self.chat_box.place(relx=0.98, rely=0.98, anchor="se") # Puts it in the very corner
        
        ctk.CTkLabel(self.chat_box, text="AI Assistant", font=("Arial", 12, "bold")).pack(pady=5)
        self.chat_display = ctk.CTkTextbox(self.chat_box, width=230, height=80)
        self.chat_display.pack(padx=10, pady=5)
        self.chat_entry = ctk.CTkEntry(self.chat_box, placeholder_text="Ask me...", width=230)
        self.chat_entry.pack(padx=10, pady=5)

    def add_subject(self):
        name = self.subject_input.get()
        if name:
            self.create_card(name)
            self.subject_input.delete(0, 'end')

    def create_card(self, name):
        card = ctk.CTkFrame(self.scroll_frame)
        card.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(card, text=name, font=("Arial", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(card, text="Log", width=60, command=lambda: print(f"Logged {name}")).pack(side="right", padx=10)