import customtkinter as ctk
import time
from datetime import datetime

# Master structured curriculum data dictionary
ACADEMIC_DATA = {
    "Bachelor of Computer Science": {
        "Year 1": ["Calculus", "Programming Fundamentals", "Discrete Structures & Probability", "Professional Development", "Computational Methods", "Object Oriented Programming & Data Structures", "Computer Architecture & Organisation", "Database Fundamentals", "Research Methodology in Computer Science", "Integrity and Leadership", "U4", "Character Building", "Sustainable Society"],
        "Year 2": ["Software Engineering Fundamentals", "Operating Systems", "Computer Networks", "Object Oriented Analysis & Design", "Algorithm Design & Analysis", "Industrial Training", "U2", "Specialisation: Software Engineering", "Specialisation: Game Development", "Specialisation: Data Science", "Specialisation: Cybersecurity"],
        "Year 3": ["Final Year Project I & II", "BYOC Electives 1-4", "U1 (x2)", "Fundamentals of Digital Competence for Programmers", "Specialisation Electives (e.g., Verification, 3D Game, Data Mining, Ethical Hacking)"]
    },
    "Bachelor of Information Technology (Information Systems)": {
        "Year 1": ["Introduction to Discrete Mathematics and Linear Algebra", "Calculus and Statistics Fundamental", "Programming Fundamentals", "Professional Development", "Management", "Object Oriented Programming and Data Structures", "Computer Architecture and Organization", "Database Fundamentals", "Fundamentals of Digital Competence for Programmers", "Integrity and Leadership", "U4", "Character Building", "Sustainable Society"],
        "Year 2": ["Software Engineering Fundamentals", "Operating Systems", "Computer Networks", "Object Oriented Analysis & Design", "IT Project Management", "Information Systems Planning and Development", "Web Application Development", "Advanced Database", "Industrial Training", "U2"],
        "Year 3": ["System Administration", "Enterprise Application Integration", "Enterprise Information Systems", "Cybersecurity: Theory and Practice", "Final Year Project I & II", "BYOC Electives 1-4", "U1 (x2)"]
    },
    "Bachelor of Information Technology (Data Communications and Networking)": {
        "Year 1": ["Computer Programming", "Database Systems", "Operating Systems", "System Analysis and Design", "Computer Architecture and Organisation", "Data Communications and Networking", "Ethics and Professional Conducts", "Discrete Mathematics and Probability", "Web Techniques and Application", "U2, U3, U4"],
        "Year 2": ["Computer Networks", "System Administration and Maintenance", "Data Structures and Algorithms", "Human Computer Interaction", "System Integration and Architecture", "Computer Security", "Artificial Intelligence Fundamentals", "Routing and Switching", "Internet of Things (IoT) Fundamental", "Network Security and Management", "Fundamentals of Digital Competence for Programmers", "U1", "BYOC Electives 1-3"],
        "Year 3": ["Enterprise Resource Planning", "Cloud Computing", "Data Analytics Fundamentals", "Mobile and Wireless Communications", "Management of Information Security", "High-Speed Network", "TCP/IP Programming", "Cloud Architecture", "Industrial Training", "Final Year Project 1 & 2"]
    },
    "Bachelor of Information Technology (Business Intelligence and Analytics)": {
        "Year 1": ["Computer Programming", "Database Systems", "Operating Systems", "System Analysis and Design", "Computer Architecture and Organisation", "Data Communications and Networking", "Ethics and Professional Conducts", "Discrete Mathematics and Probability", "Web Techniques and Application", "U1, U3, U4"],
        "Year 2": ["Computer Networks", "System Administration and Maintenance", "Data Structures and Algorithms", "Human Computer Interaction", "System Integration and Architecture", "Computer Security", "Artificial Intelligence Fundamentals", "Business Statistical Analysis", "Internet of Things (IoT) Fundamental", "Business Intelligence", "Fundamentals of Digital Competence for Programmers", "U1", "BYOC Electives 1-3"],
        "Year 3": ["Enterprise Resource Planning", "Cloud Computing", "Data Analytics Fundamentals", "Data Storytelling", "Management of Information Security", "Internet Marketing", "Project Management for Business Analysts", "Data Mining and Machine Learning", "Industrial Training", "Final Year Project 1 & 2"]
    },
    "Bachelor of Computer Science (Artificial Intelligence)": {
        "Year 1": ["Computer Architecture and Organisation", "Data Communications and Networking", "Computer Programming", "Database Systems", "Operating Systems", "System Analysis and Design", "Ethics and Professional Conducts", "Discrete Mathematics and Probability", "Web Techniques and Application", "U2, U3, U4", "Character Building", "Sustainable Society"],
        "Year 2": ["Human Computer Interaction", "Software Engineering Fundamentals", "Programming Language Concept", "Artificial Intelligence Fundamentals", "Data Structures and Algorithms", "Computer Networks", "Semantic Web Technology", "Machine Learning", "Computer Graphics", "Data Analytics Fundamentals", "Fundamentals of Digital Competence for Programmers", "Electives 1-3", "U1"],
        "Year 3": ["Parallel Computing", "Algorithm Design and Analysis", "Data Wrangling and Visualization", "Natural Language Processing", "Cloud Computing", "Expert Systems", "Computational Intelligence", "Computer Vision", "Industrial Training", "Project I & II"]
    },
    "Bachelor of Information Technology (Security Technology)": {
        "Year 1": ["Web Techniques and Application", "Computer Architecture and Organisation", "Data Comm and Networking", "Comp Programming", "Database Systems", "Operating Systems", "System Analysis and Design", "Ethics and Professional Conduct", "Discrete Mathematics and Probability", "U1, U3, U4", "Character Building", "Sustainable Society"],
        "Year 2": ["Human Computer Interaction", "System Integration and Architecture", "Computer Security", "System Administration and Maintenance", "Data Structures and Algorithms", "Cybersecurity Law", "Ethical Hacking and Security Assessment", "Information Assurance and Security", "Applied Cryptography", "Fundamentals of Digital Competence for Programmers", "BYOC Electives 1-3", "U1"],
        "Year 3": ["Enterprise Resource Planning", "Cloud computing", "Management of Information Security", "Malware and Intrusion Detection", "Password Authentication and biometrics", "Digital Forensics", "Security Analysis and Vulnerability Assessment", "Python for Security", "Industrial Training", "Project 1 & 2"]
    }
}


class CTkTooltip:
    """A lightweight tooltip handler that spawns a small panel near the cursor on hover."""
    def __init__(self, widget, get_text_callback):
        self.widget = widget
        self.get_text_callback = get_text_callback
        self.tooltip_window = None
        
        # Bind hover events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        text = self.get_text_callback()
        if not text:
            return
            
        self.hide_tooltip()

        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True) 
        
        frame = ctk.CTkFrame(self.tooltip_window, fg_color="#131C32", border_width=1, border_color="#00F0FF")
        frame.pack()
        
        label = ctk.CTkLabel(frame, text=text, font=("Arial", 11), text_color="#FFFFFF", wraplength=250, justify="left")
        label.pack(padx=8, pady=5)

        x = self.widget.winfo_pointerx() + 15
        y = self.widget.winfo_pointery() + 10
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class LogSessionWindow(ctk.CTkToplevel):
    def __init__(self, parent, subject_name, completion_callback):
        super().__init__(parent, fg_color="#0A0F1D")
        self.title(f"Timer: {subject_name}")
        self.geometry("350x250")
        self.resizable(False, False)
        
        self.lift()
        self.grab_set()

        self.subject_name = subject_name
        self.completion_callback = completion_callback
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False

        ctk.CTkLabel(self, text=subject_name, font=("Arial", 15, "bold"), text_color="#FFFFFF", wraplength=300).pack(pady=15)
        
        self.time_label = ctk.CTkLabel(self, text="00:00:00", font=("Arial", 38, "bold"), text_color="#00F0FF")
        self.time_label.pack(pady=10)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=15)

        self.start_btn = ctk.CTkButton(self.btn_frame, text="Start", width=110, height=35, fg_color="#1F2E54", text_color="#00F0FF", hover_color="#2D437A", command=self.toggle_timer)
        self.start_btn.pack(side="left", padx=5)

        self.save_btn = ctk.CTkButton(self.btn_frame, text="Save Log", width=110, height=35, fg_color="#00F0FF", text_color="#0A0F1D", hover_color="#00C8D6", state="disabled", command=self.save_session)
        self.save_btn.pack(side="left", padx=5)

    def toggle_timer(self):
        if not self.running:
            self.running = True
            self.start_btn.configure(text="Pause", fg_color="#FFCC00", text_color="#0A0F1D", hover_color="#E6B800")
            self.save_btn.configure(state="disabled")
            self.start_time = time.time() - self.elapsed_time
            self.update_timer_loop()
        else:
            self.running = False
            self.start_btn.configure(text="Resume", fg_color="#1F2E54", text_color="#00F0FF", hover_color="#2D437A")
            self.save_btn.configure(state="normal")

    def update_timer_loop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(int(self.elapsed_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.after(1000, self.update_timer_loop)

    def save_session(self):
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hours, remainder = divmod(int(self.elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
        self.completion_callback(self.subject_name, current_timestamp, duration_str)
        self.destroy()


class MainPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0A0F1D")

        # Layout grids configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1) 

        self.degree_map = {}
        self.subject_map = {}

        # --- 1. SIDEBAR CONFIGURATION ---
        self.sidebar = ctk.CTkFrame(self, width=230, fg_color="#0D1527", border_width=1, border_color="#1F2E54")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.sidebar.grid_propagate(False) 
        
        ctk.CTkLabel(self.sidebar, text="Course Selection", font=("Arial", 18, "bold"), text_color="#00F0FF").pack(pady=(25, 20))

        dropdown_kwargs = {
            "width": 200, "height": 35, "fg_color": "#131C32", "button_color": "#1F2E54",
            "button_hover_color": "#2D437A", "text_color": "#FFFFFF", "dropdown_fg_color": "#131C32",
            "dropdown_text_color": "#FFFFFF", "dropdown_hover_color": "#1F2E54"
        }

        # Degree UI Elements
        ctk.CTkLabel(self.sidebar, text="Select Degree:", font=("Arial", 12), text_color="#8A99AD").pack(anchor="w", padx=15)
        display_degrees = [self.truncate_text(name, 24) for name in ACADEMIC_DATA.keys()]
        for full, short in zip(ACADEMIC_DATA.keys(), display_degrees):
            self.degree_map[short] = full

        self.degree_dropdown = ctk.CTkOptionMenu(self.sidebar, values=display_degrees, command=self.update_years, **dropdown_kwargs)
        self.degree_dropdown.pack(pady=(0, 15), padx=15)
        CTkTooltip(self.degree_dropdown, lambda: self.degree_map.get(self.degree_dropdown.get()))

        # Year UI Elements
        ctk.CTkLabel(self.sidebar, text="Select Year:", font=("Arial", 12), text_color="#8A99AD").pack(anchor="w", padx=15)
        self.year_dropdown = ctk.CTkOptionMenu(self.sidebar, values=[], command=self.update_subjects, **dropdown_kwargs)
        self.year_dropdown.pack(pady=(0, 15), padx=15)

        # Subject UI Elements
        ctk.CTkLabel(self.sidebar, text="Select Subject:", font=("Arial", 12), text_color="#8A99AD").pack(anchor="w", padx=15)
        self.subject_dropdown = ctk.CTkOptionMenu(self.sidebar, values=[], **dropdown_kwargs)
        self.subject_dropdown.pack(pady=(0, 25), padx=15)
        CTkTooltip(self.subject_dropdown, lambda: self.subject_map.get(self.subject_dropdown.get()))

        self.add_btn = ctk.CTkButton(self.sidebar, text="Add to Dashboard", font=("Arial", 13, "bold"), width=200, height=40, fg_color="#00F0FF", hover_color="#00C8D6", text_color="#0A0F1D", command=self.add_selected_subject)
        self.add_btn.pack(pady=5, padx=15)

        # --- 2. ACTIVE CARDS TRACKER PANEL ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Your Active Studies", fg_color="#0A0F1D", label_text_color="#8A99AD")
        self.scroll_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # --- 3. MASTERY GRAPH HOUSING AREA ---
        self.graph_frame = ctk.CTkFrame(self, fg_color="#0D1527", border_width=1, border_color="#1F2E54")
        self.graph_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(self.graph_frame, text="Mastery Score Graph", font=("Arial", 16, "bold"), text_color="#FFFFFF").pack(pady=10)
        
        self.graph_canvas = ctk.CTkFrame(self.graph_frame, fg_color="#060A12", height=200)
        self.graph_canvas.pack(fill="both", expand=True, padx=20, pady=10)

        # --- 4. FLOATING SYSTEM ASSISTANT OVERLAY ---
        self.chat_box = ctk.CTkFrame(self, width=260, height=160, fg_color="#0D1527", border_width=1, border_color="#00F0FF")
        self.chat_box.place(relx=0.98, rely=0.98, anchor="se")
        
        ctk.CTkLabel(self.chat_box, text="AI Assistant", font=("Arial", 12, "bold"), text_color="#00F0FF").pack(pady=3)
        self.chat_display = ctk.CTkTextbox(self.chat_box, width=240, height=80, fg_color="#060A12", text_color="#FFFFFF", border_width=1, border_color="#1F2E54")
        self.chat_display.pack(padx=10, pady=2)
        self.chat_entry = ctk.CTkEntry(self.chat_box, placeholder_text="Ask me...", width=240, fg_color="#131C32", text_color="#FFFFFF", border_color="#1F2E54")
        self.chat_entry.pack(padx=10, pady=5)

        # Build initial dependencies loop structure
        self.update_years(self.degree_dropdown.get())

    def truncate_text(self, text, limit=24):
        return text[:limit].strip() + "..." if len(text) > limit else text

    def update_years(self, selected_short_degree):
        full_degree = self.degree_map.get(selected_short_degree)
        if full_degree:
            years = list(ACADEMIC_DATA[full_degree].keys())
            self.year_dropdown.configure(values=years)
            self.year_dropdown.set(years[0])
            self.update_subjects(years[0])

    def update_subjects(self, selected_year):
        short_degree = self.degree_dropdown.get()
        full_degree = self.degree_map.get(short_degree)
        if not full_degree: return

        raw_subjects = ACADEMIC_DATA[full_degree][selected_year]
        self.subject_map.clear()
        display_subjects = []

        for item in raw_subjects:
            short_sub = self.truncate_text(item, limit=24)
            display_subjects.append(short_sub)
            self.subject_map[short_sub] = item

        self.subject_dropdown.configure(values=display_subjects)
        self.subject_dropdown.set(display_subjects[0])

    def add_selected_subject(self):
        short_subject = self.subject_dropdown.get()
        full_subject = self.subject_map.get(short_subject)
        if full_subject:
            self.create_card(full_subject)

    def open_tracker(self, subject_name):
        LogSessionWindow(self, subject_name, self.handle_logged_session)

    def handle_logged_session(self, subject, timestamp, duration):
        self.chat_display.insert("end", f"\n[{timestamp.split()[0]}] Tracked {duration} -> {self.truncate_text(subject, 12)}")

    def create_card(self, name):
        card = ctk.CTkFrame(self.scroll_frame, fg_color="#0D1527", border_width=1, border_color="#1F2E54")
        card.pack(fill="x", pady=5, padx=5)
        
        lbl = ctk.CTkLabel(card, text=self.truncate_text(name, 28), font=("Arial", 13, "bold"), text_color="#FFFFFF")
        lbl.pack(side="left", padx=15, pady=12)
        CTkTooltip(lbl, lambda: name)
        
        start_session_btn = ctk.CTkButton(
            card, text="Start Session", width=110, height=30,
            fg_color="#1F2E54", text_color="#00F0FF", hover_color="#2D437A",
            command=lambda: self.open_tracker(name)
        )
        start_session_btn.pack(side="right", padx=15, pady=12)