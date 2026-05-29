import customtkinter as ctk
import time
from datetime import datetime

# Master structured curriculum data dictionary
ACADEMIC_DATA = {
    "Bachelor of Computer Science": {
        "Year 1": [
            "Calculus", "Programming Fundamentals", "Discrete Structures & Probability",
            "Professional Development", "Computational Methods", "Object Oriented Programming & Data Structures",
            "Computer Architecture & Organisation", "Database Fundamentals", "Research Methodology in Computer Science",
            "Integrity and Leadership", "U4", "Character Building", "Sustainable Society"
        ],
        "Year 2": [
            "Software Engineering Fundamentals", "Operating Systems", "Computer Networks",
            "Object Oriented Analysis & Design", "Algorithm Design & Analysis", "Industrial Training", "U2",
            "Specialisation: Software Engineering", "Specialisation: Game Development", 
            "Specialisation: Data Science", "Specialisation: Cybersecurity"
        ],
        "Year 3": [
            "Final Year Project I & II", "BYOC Electives 1-4", "U1 (x2)",
            "Fundamentals of Digital Competence for Programmers",
            "Specialisation Electives (e.g., Verification, 3D Game, Data Mining, Ethical Hacking)"
        ]
    },
    "Bachelor of Information Technology (Information Systems)": {
        "Year 1": [
            "Introduction to Discrete Mathematics and Linear Algebra", "Calculus and Statistics Fundamental",
            "Programming Fundamentals", "Professional Development", "Management",
            "Object Oriented Programming and Data Structures", "Computer Architecture and Organization",
            "Database Fundamentals", "Fundamentals of Digital Competence for Programmers",
            "Integrity and Leadership", "U4", "Character Building", "Sustainable Society"
        ],
        "Year 2": [
            "Software Engineering Fundamentals", "Operating Systems", "Computer Networks",
            "Object Oriented Analysis & Design", "IT Project Management", "Information Systems Planning and Development",
            "Web Application Development", "Advanced Database", "Industrial Training", "U2"
        ],
        "Year 3": [
            "System Administration", "Enterprise Application Integration", "Enterprise Information Systems",
            "Cybersecurity: Theory and Practice", "Final Year Project I & II", "BYOC Electives 1-4", "U1 (x2)"
        ]
    },
    "Bachelor of Information Technology (Data Communications and Networking)": {
        "Year 1": [
            "Computer Programming", "Database Systems", "Operating Systems", "System Analysis and Design",
            "Computer Architecture and Organisation", "Data Communications and Networking", "Ethics and Professional Conducts",
            "Discrete Mathematics and Probability", "Web Techniques and Application", "U2, U3, U4"
        ],
        "Year 2": [
            "Computer Networks", "System Administration and Maintenance", "Data Structures and Algorithms",
            "Human Computer Interaction", "System Integration and Architecture", "Computer Security",
            "Artificial Intelligence Fundamentals", "Routing and Switching", "Internet of Things (IoT) Fundamental",
            "Network Security and Management", "Fundamentals of Digital Competence for Programmers", "U1", "BYOC Electives 1-3"
        ],
        "Year 3": [
            "Enterprise Resource Planning", "Cloud Computing", "Data Analytics Fundamentals",
            "Mobile and Wireless Communications", "Management of Information Security", "High-Speed Network",
            "TCP/IP Programming", "Cloud Architecture", "Industrial Training", "Final Year Project 1 & 2"
        ]
    },
    "Bachelor of Information Technology (Business Intelligence and Analytics)": {
        "Year 1": [
            "Computer Programming", "Database Systems", "Operating Systems", "System Analysis and Design",
            "Computer Architecture and Organisation", "Data Communications and Networking", "Ethics and Professional Conducts",
            "Discrete Mathematics and Probability", "Web Techniques and Application", "U1, U3, V4"
        ],
        "Year 2": [
            "Computer Networks", "System Administration and Maintenance", "Data Structures and Algorithms",
            "Human Computer Interaction", "System Integration and Architecture", "Computer Security",
            "Artificial Intelligence Fundamentals", "Business Statistical Analysis", "Internet of Things (IoT) Fundamental",
            "Business Intelligence", "Fundamentals of Digital Competence for Programmers", "U1", "BYOC Electives 1-3"
        ],
        "Year 3": [
            "Enterprise Resource Planning", "Cloud Computing", "Data Analytics Fundamentals", "Data Storytelling",
            "Management of Information Security", "Internet Marketing", "Project Management for Business Analysts",
            "Data Mining and Machine Learning", "Industrial Training", "Final Year Project 1 & 2"
        ]
    },
    "Bachelor of Computer Science (Artificial Intelligence)": {
        "Year 1": [
            "Computer Architecture and Organisation", "Data Communications and Networking", "Computer Programming",
            "Database Systems", "Operating Systems", "System Analysis and Design", "Ethics and Professional Conducts",
            "Discrete Mathematics and Probability", "Web Techniques and Application", "U2, U3, U4", "Character Building", "Sustainable Society"
        ],
        "Year 2": [
            "Human Computer Interaction", "Software Engineering Fundamentals", "Programming Language Concept",
            "Artificial Intelligence Fundamentals", "Data Structures and Algorithms", "Computer Networks",
            "Semantic Web Technology", "Machine Learning", "Computer Graphics", "Data Analytics Fundamentals",
            "Fundamentals of Digital Competence for Programmers", "Electives 1-3", "U1"
        ],
        "Year 3": [
            "Parallel Computing", "Algorithm Design and Analysis", "Data Wrangling and Visualization",
            "Natural Language Processing", "Cloud Computing", "Expert Systems", "Computational Intelligence",
            "Computer Vision", "Industrial Training", "Project I & II"
        ]
    },
    "Bachelor of Information Technology (Security Technology)": {
        "Year 1": [
            "Web Techniques and Application", "Computer Architecture and Organisation", "Data Comm and Networking",
            "Comp Programming", "Database Systems", "Operating Systems", "System Analysis and Design",
            "Ethics and Professional Conduct", "Discrete Mathematics and Probability", "U1, U3, U4", "Character Building", "Sustainable Society"
        ],
        "Year 2": [
            "Human Computer Interaction", "System Integration and Architecture", "Computer Security",
            "System Administration and Maintenance", "Data Structures and Algorithms", "Cybersecurity Law",
            "Ethical Hacking and Security Assessment", "Information Assurance and Security", "Applied Cryptography",
            "Fundamentals of Digital Competence for Programmers", "BYOC Electives 1-3", "U1"
        ],
        "Year 3": [
            "Enterprise Resource Planning", "Cloud computing", "Management of Information Security",
            "Malware and Intrusion Detection", "Password Authentication and biometrics", "Digital Forensics",
            "Security Analysis and Vulnerability Assessment", "Python for Security", "Industrial Training", "Project 1 & 2"
        ]
    }
}


class LogSessionWindow(ctk.CTkToplevel):
    """A Toplevel popup window acting as a stopwatch to log study sessions."""
    def __init__(self, parent, subject_name, completion_callback):
        super().__init__(parent)
        self.title(f"Session Tracker: {subject_name}")
        self.geometry("350x250")
        self.resizable(False, False)
        
        # Ensure focus rests on popup modal
        self.lift()
        self.grab_set()

        self.subject_name = subject_name
        self.completion_callback = completion_callback
        
        # Tracking states
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False

        # UI Elements
        ctk.CTkLabel(self, text=subject_name, font=("Arial", 16, "bold"), wraplength=300).pack(pady=10)
        
        self.time_label = ctk.CTkLabel(self, text="00:00:00", font=("Arial", 36, "bold"))
        self.time_label.pack(pady=15)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.start_btn = ctk.CTkButton(self.btn_frame, text="Start", width=100, command=self.toggle_timer)
        self.start_btn.pack(side="left", padx=5)

        self.save_btn = ctk.CTkButton(self.btn_frame, text="Save Log", width=100, state="disabled", command=self.save_session)
        self.save_btn.pack(side="left", padx=5)

    def toggle_timer(self):
        """Starts or pauses the duration tracking timer clock."""
        if not self.running:
            self.running = True
            self.start_btn.configure(text="Pause", fg_color="goldenrod", hover_color="darkgoldenrod")
            self.save_btn.configure(state="disabled")
            self.start_time = time.time() - self.elapsed_time
            self.update_timer_loop()
        else:
            self.running = False
            self.start_btn.configure(text="Resume", fg_color="#1f538d", hover_color="#14375e")
            self.save_btn.configure(state="normal")

    def update_timer_loop(self):
        """Internal recursive UI loop updating timer display labels."""
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            
            # Format time as hours:minutes:seconds
            hours, remainder = divmod(int(self.elapsed_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            self.time_label.configure(text=time_str)
            self.after(1000, self.update_timer_loop)

    def save_session(self):
        """Generates exact localized system timestamps and returns the record."""
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        hours, remainder = divmod(int(self.elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"

        # Pass data payload back to MainPage handler
        self.completion_callback(self.subject_name, current_timestamp, duration_str)
        self.destroy()


class MainPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Main window structural grid layouts
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1) 

        # State dictionaries to reverse map short display strings back to full raw names
        self.degree_map = {}
        self.subject_map = {}

        # --- 1. SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.sidebar.grid_propagate(False) 
        
        ctk.CTkLabel(self.sidebar, text="Course Selection", font=("Arial", 18, "bold")).pack(pady=(20, 15))

        # Degree UI Elements
        ctk.CTkLabel(self.sidebar, text="Select Degree:", font=("Arial", 12)).pack(anchor="w", padx=15)
        
        display_degrees = []
        for full_name in ACADEMIC_DATA.keys():
            short_name = self.truncate_text(full_name, limit=24)
            display_degrees.append(short_name)
            self.degree_map[short_name] = full_name

        self.degree_dropdown = ctk.CTkOptionMenu(
            self.sidebar, 
            values=display_degrees,
            command=self.update_years,
            width=190
        )
        self.degree_dropdown.pack(pady=(0, 15), padx=15)

        # Year UI Elements
        ctk.CTkLabel(self.sidebar, text="Select Year:", font=("Arial", 12)).pack(anchor="w", padx=15)
        self.year_dropdown = ctk.CTkOptionMenu(
            self.sidebar, 
            values=[], 
            command=self.update_subjects,
            width=190
        )
        self.year_dropdown.pack(pady=(0, 15), padx=15)

        # Subject UI Elements
        ctk.CTkLabel(self.sidebar, text="Select Subject:", font=("Arial", 12)).pack(anchor="w", padx=15)
        self.subject_dropdown = ctk.CTkOptionMenu(
            self.sidebar, 
            values=[],
            width=190
        )
        self.subject_dropdown.pack(pady=(0, 20), padx=15)

        self.add_btn = ctk.CTkButton(self.sidebar, text="Add to Dashboard", command=self.add_selected_subject, width=190)
        self.add_btn.pack(pady=5, padx=15)

        # --- 2. ACTIVE CARDS TRACKER AREA ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Your Active Studies")
        self.scroll_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # --- 3. GRAPH HOUSING AREA ---
        self.graph_frame = ctk.CTkFrame(self, fg_color="gray20")
        self.graph_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(self.graph_frame, text="Mastery Score Graph", font=("Arial", 16)).pack(pady=10)
        
        self.graph_canvas = ctk.CTkFrame(self.graph_frame, fg_color="black", height=200)
        self.graph_canvas.pack(fill="both", expand=True, padx=20, pady=10)

        # --- 4. FLOATING CHAT WIDGET ---
        self.chat_box = ctk.CTkFrame(self, width=250, height=150, border_width=2, border_color="cyan")
        self.chat_box.place(relx=0.98, rely=0.98, anchor="se")
        
        ctk.CTkLabel(self.chat_box, text="AI Assistant", font=("Arial", 12, "bold")).pack(pady=5)
        self.chat_display = ctk.CTkTextbox(self.chat_box, width=230, height=80)
        self.chat_display.pack(padx=10, pady=5)
        self.chat_entry = ctk.CTkEntry(self.chat_box, placeholder_text="Ask me...", width=230)
        self.chat_entry.pack(padx=10, pady=5)

        # Initialize Cascade system choices
        self.update_years(self.degree_dropdown.get())

    def truncate_text(self, text, limit=24):
        if len(text) > limit:
            return text[:limit].strip() + "..."
        return text

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
        if not full_degree:
            return

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
        """Creates the stopwatch window modal instance."""
        LogSessionWindow(self, subject_name, self.handle_logged_session)

    def handle_logged_session(self, subject, timestamp, duration):
        """Callback that receives data from popup when user completes a study track."""
        print(f"[{timestamp}] Logged: {subject} | Duration: {duration}")
        # Placeholder context to print logs inside the Chatbot frame display box for verification
        self.chat_display.insert("end", f"\nLogged {duration} for {self.truncate_text(subject, 15)} on {timestamp.split()[0]}")

    def create_card(self, name):
        """Creates dynamic subject tracking rows containing a start session option trigger."""
        card = ctk.CTkFrame(self.scroll_frame)
        card.pack(fill="x", pady=5, padx=5)
        
        # Display name label
        ctk.CTkLabel(card, text=name, font=("Arial", 14, "bold")).pack(side="left", padx=10, pady=10)
        
        # Session stopwatch generation control button
        start_session_btn = ctk.CTkButton(
            card, 
            text="Start Session", 
            width=100, 
            command=lambda: self.open_tracker(name)
        )
        start_session_btn.pack(side="right", padx=10, pady=10)