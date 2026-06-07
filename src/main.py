import customtkinter as ctk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- MODULE IMPORTS ---
from timer import FocusTimerWindow
from heatmap_ui import ActivityHeatmap

# ==========================================
# 1. CORE MATH & ALGORITHM ENGINE
# ==========================================
def calculate_time_decay(current_score, last_studied_date_str):
    if not last_studied_date_str:
        return current_score, 0.0

    last_studied = datetime.strptime(last_studied_date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    days_passed = (today - last_studied).days

    if days_passed > 7:
        weeks_missed = days_passed // 7
        penalty = weeks_missed * 5.0
        return round(max(current_score - penalty, 0.0), 1), penalty
    return current_score, 0.0

def get_algorithmic_insights(duration_mins, confidence_level, penalty):
    insights = []
    if penalty >= 10.0:
        insights.append("🔴 CRITICAL DECAY: High memory loss detected. Immediate review required.")
    elif penalty > 0.0:
        insights.append("🟡 WARNING: Memory decay has started. Schedule a review session within 48 hours.")
    else:
        insights.append("🟢 OPTIMAL: You are studying within the ideal spaced-repetition window.")

    if duration_mins > 90:
        insights.append("🧠 EFFICIENCY DROP: Sessions over 90 mins risk cognitive burnout. Take breaks.")
    elif duration_mins < 20:
        insights.append("⏱️ MICRO-SESSION: Session is too short for deep cognitive work. Aim for 25+ mins.")

    if confidence_level <= 2:
        insights.append("📚 STRATEGY: Low confidence. Shift focus from passive reading to active recall.")
    elif confidence_level >= 4:
        insights.append("🚀 MASTERY: High confidence. Begin testing yourself with past year exam papers.")

    return "\n\n".join(insights)

# ==========================================
# 2. MMU FOUNDATION CURRICULUM DATABASE
# ==========================================
MMU_COURSES = {
    "Foundation in Computing": {
        "Trimester 1": ["Intro to Computing Technologies", "Communicative English", "Mathematics I"],
        "Trimester 2": ["Essential English", "Multimedia Fundamentals", "Mathematics II", "Intro to Business Management", "Problem Solving and Program Design" ],
        "Trimester 3": ["Academic English", "Mathematics III", "Mini IT Project", "Critical Thinking", "Intro to Digital Systems", "Principle of Physics"]
    },
    "Foundation in Engineering": {
        "Trimester 1": ["Algebra and Trigonometry", "Mechanics", "Communicative English", "Critical Thinking", "Physical Computing"],
        "Trimester 2": ["Calculus and Linear Algebra", "Essential English", "Chemistry", "Electricity and Magnetism", "Intro to Business Management", "STEM Project"],
        "Trimester 3": ["Academic English", "Modern Physics and Thermodynamics", "Intro to Probability and Statistics"]
    },
    "Foundation in Science and Technology": {
        "Trimester 1": ["Communicative English", "Creative and Critical Thinking", "Foundation Math 1", "Intro to Computing and Technology", "Basic of Computer System Design", "Mechanics & Thermodynamics"],
        "Trimester 2": ["Essential English", "Intro to Probability and Statistics", "Intro to Physics", "Waves & Modern Physics"],
        "Trimester 3": ["Academic English", "Fundamental of Business Management", "Foundation Math 2", "Basic Database", "Problem Solving and Programming", "Electricity & Magnetism", "Chemistry"]
    },
    "Foundation in Creative Multimedia": {
        "Trimester 1": ["Visual Research & Comm 1", "Life Drawing", "Basic Photography", "Computer Graphics 1", "Basic Sound Design", "Popular Culture Studies"],
        "Trimester 2": ["Storytelling and Mythology"],
        "Trimester 3": ["Visual Research & Comm 2", "Figure Drawing", "Creative Photography", "Computer Graphics 2", "Design & Art Appreciation", "Critical Thinking & Reasoning"]
    },
    "Foundation in Communication": {
        "Trimester 1": ["Communicative English", "Communication Studies", "Fundamentals of Visual Comm", "Discovering Mass Comm", "Reasoning and Advocacy", "Fundamentals of Media Writing"],
        "Trimester 2": ["Social and Emotional Health", "Public Speaking", "Essential English", "Communication and Culture", "Intro to Digital Content Entrepreneurship", "Digital Media Applications", "Social Network Application"],
        "Trimester 3": ["Academic English", "Fundamentals of Integrated Marketing", "Fundamentals of Digital Journalism"]
    },
    "Foundation in Law": {
        "Trimester 1": ["Communicative English", "Critical Thinking", "Computer Applications", "Intro to Law", "General Principles of Law", "Malaysian Legal History"],
        "Trimester 2": ["Essential English", "Fundamentals of Business Management", "Basic Accounting for Lawyers", "Intro to Criminal and Constitutional Law", "Intro to Politics and Governance", "Intro to Syariah Law"],
        "Trimester 3": ["English for Law", "Law and Society", "Intro to Commercial Law"]
    }
}

# ==========================================
# 3. THE MULTI-PAGE APPLICATION
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class NexusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexus - Student Operating System")
        self.geometry("1100x750")

        self.mock_database = {
            "Mathematics I": {"duration": 60, "confidence": 4, "old_score": 85.0, "days_ago": 8},
            "Problem Solving and Program Design": {"duration": 120, "confidence": 2, "old_score": 60.0, "days_ago": 15},
            "Intro to Business Management": {"duration": 30, "confidence": 5, "old_score": 95.0, "days_ago": 2}
        }
        self.subject_list = list(self.mock_database.keys())

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- NAVIGATION SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar_frame, text="NEXUS", font=("Helvetica", 28, "bold"), text_color="#3498db").pack(pady=(30, 40))

        # Added Home Dashboard Button
        self.btn_nav_home = ctk.CTkButton(self.sidebar_frame, text="🏠 Home Dashboard", command=lambda: self.show_page("home"), fg_color="transparent", border_width=1, hover_color="#2c3e50")
        self.btn_nav_home.pack(pady=10, padx=20, fill="x")

        self.btn_nav_input = ctk.CTkButton(self.sidebar_frame, text="📝 Log Study Session", command=lambda: self.show_page("input"), fg_color="transparent", border_width=1, hover_color="#2c3e50")
        self.btn_nav_input.pack(pady=10, padx=20, fill="x")

        self.btn_nav_analytics = ctk.CTkButton(self.sidebar_frame, text="📊 View Analytics", command=lambda: self.show_page("analytics"), fg_color="transparent", border_width=1, hover_color="#2c3e50")
        self.btn_nav_analytics.pack(pady=10, padx=20, fill="x")

        # --- PAGE CONTAINERS ---
        self.home_page = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")
        self.input_page = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")
        self.analytics_page = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")

        self.build_home_page()
        self.build_input_page()
        self.build_analytics_page()

        # Start on the Home Dashboard
        self.show_page("home")

    def show_page(self, page_name):
        self.home_page.grid_forget()
        self.input_page.grid_forget()
        self.analytics_page.grid_forget()

        if page_name == "home":
            self.home_page.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif page_name == "input":
            self.input_page.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif page_name == "analytics":
            self.analytics_page.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.analytics_dropdown.set(self.subject_list[0])
            self.refresh_analytics(self.subject_list[0]) 

    # ------------------------------------------
    # PAGE 1: HOME DASHBOARD (NEW)
    # ------------------------------------------
    def build_home_page(self):
        # Welcome Banner
        ctk.CTkLabel(self.home_page, text="Welcome back, Scholar.", font=("Helvetica", 32, "bold")).pack(pady=(40, 10))
        ctk.CTkLabel(self.home_page, text="Here is your study overview for this month.", font=("Helvetica", 16), text_color="gray").pack(pady=(0, 30))

        # Top Metrics Frame
        metrics_frame = ctk.CTkFrame(self.home_page, fg_color="transparent")
        metrics_frame.pack(pady=10, fill="x", padx=50)

        # Metric 1: Total Hours
        card1 = ctk.CTkFrame(metrics_frame, fg_color="#2b2b2b", corner_radius=15, width=200, height=100)
        card1.pack(side="left", expand=True, padx=10)
        card1.pack_propagate(False)
        ctk.CTkLabel(card1, text="Total Study Hours", font=("Helvetica", 14), text_color="gray").pack(pady=(15, 5))
        ctk.CTkLabel(card1, text="32.5 hrs", font=("Helvetica", 28, "bold"), text_color="#3498db").pack()

        # Metric 2: Current Streak
        card2 = ctk.CTkFrame(metrics_frame, fg_color="#2b2b2b", corner_radius=15, width=200, height=100)
        card2.pack(side="left", expand=True, padx=10)
        card2.pack_propagate(False)
        ctk.CTkLabel(card2, text="Current Streak", font=("Helvetica", 14), text_color="gray").pack(pady=(15, 5))
        ctk.CTkLabel(card2, text="4 Days 🔥", font=("Helvetica", 28, "bold"), text_color="#e67e22").pack()

        # Metric 3: Subjects Tracked
        card3 = ctk.CTkFrame(metrics_frame, fg_color="#2b2b2b", corner_radius=15, width=200, height=100)
        card3.pack(side="left", expand=True, padx=10)
        card3.pack_propagate(False)
        ctk.CTkLabel(card3, text="Subjects Tracked", font=("Helvetica", 14), text_color="gray").pack(pady=(15, 5))
        ctk.CTkLabel(card3, text=f"{len(self.subject_list)}", font=("Helvetica", 28, "bold"), text_color="#2ecc71").pack()

        # PLUG IN THE HEATMAP MODULE!
        ctk.CTkLabel(self.home_page, text="Consistency Heatmap", font=("Helvetica", 18, "bold")).pack(pady=(40, 10))
        self.heatmap_widget = ActivityHeatmap(self.home_page)
        self.heatmap_widget.pack(pady=10, padx=50, fill="x")

    # ------------------------------------------
    # PAGE 2: DATA ENTRY (Tabbed Interface)
    # ------------------------------------------
    def build_input_page(self):
        ctk.CTkLabel(self.input_page, text="Log Study Session", font=("Helvetica", 32, "bold")).pack(pady=(20, 10))

        dropdown_frame = ctk.CTkFrame(self.input_page, fg_color="transparent")
        dropdown_frame.pack(pady=10)

        ctk.CTkLabel(dropdown_frame, text="Program:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        programs = list(MMU_COURSES.keys())
        self.var_program = ctk.CTkOptionMenu(dropdown_frame, values=programs, width=300, command=self.update_trimesters)
        self.var_program.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(dropdown_frame, text="Trimester:", font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.var_trimester = ctk.CTkOptionMenu(dropdown_frame, values=[], width=300, command=self.update_subjects)
        self.var_trimester.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(dropdown_frame, text="Subject:", font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.var_subject = ctk.CTkOptionMenu(dropdown_frame, values=[], width=300)
        self.var_subject.grid(row=2, column=1, padx=10, pady=5)

        self.var_program.set(programs[0])
        self.update_trimesters(programs[0])

        self.log_tabs = ctk.CTkTabview(self.input_page, width=450, height=250)
        self.log_tabs.pack(pady=20)
        
        self.log_tabs.add("⏱️ Active Timer")
        self.log_tabs.add("📝 Manual Entry")

        ctk.CTkLabel(self.log_tabs.tab("⏱️ Active Timer"), text="Study with the app open to track exact time.", text_color="gray").pack(pady=(20, 10))
        ctk.CTkButton(self.log_tabs.tab("⏱️ Active Timer"), text="Launch Focus Timer", height=50, width=250, font=("Helvetica", 16, "bold"), fg_color="#3498db", hover_color="#2980b9", command=self.open_timer).pack(pady=20)

        ctk.CTkLabel(self.log_tabs.tab("📝 Manual Entry"), text="Duration (Minutes):", font=("Helvetica", 14)).pack(pady=(10, 0))
        self.var_duration = ctk.CTkSlider(self.log_tabs.tab("📝 Manual Entry"), from_=10, to=180, number_of_steps=34, width=300)
        self.var_duration.set(60)
        self.var_duration.pack(pady=5)
        
        self.label_duration_val = ctk.CTkLabel(self.log_tabs.tab("📝 Manual Entry"), text="60 mins", text_color="#3498db", font=("Helvetica", 12, "bold"))
        self.label_duration_val.pack()
        self.var_duration.configure(command=lambda val: self.label_duration_val.configure(text=f"{int(val)} mins"))

        ctk.CTkLabel(self.log_tabs.tab("📝 Manual Entry"), text="Confidence Level (1-5):", font=("Helvetica", 14)).pack(pady=(10, 0))
        self.var_confidence = ctk.CTkSlider(self.log_tabs.tab("📝 Manual Entry"), from_=1, to=5, number_of_steps=4, width=300)
        self.var_confidence.set(3)
        self.var_confidence.pack(pady=5)

        self.label_conf_val = ctk.CTkLabel(self.log_tabs.tab("📝 Manual Entry"), text="Level 3", text_color="#3498db", font=("Helvetica", 12, "bold"))
        self.label_conf_val.pack()
        self.var_confidence.configure(command=lambda val: self.label_conf_val.configure(text=f"Level {int(val)}"))

        ctk.CTkButton(self.log_tabs.tab("📝 Manual Entry"), text="Save Manual Log", height=35, width=200, fg_color="#2ecc71", hover_color="#27ae60", command=self.save_session).pack(pady=10)

    # --- CONTROLLER LOGIC FOR INPUT PAGE ---
    def update_trimesters(self, selected_program):
        trimesters = list(MMU_COURSES[selected_program].keys())
        self.var_trimester.configure(values=trimesters)
        self.var_trimester.set(trimesters[0])
        self.update_subjects(trimesters[0])

    def update_subjects(self, selected_trimester):
        selected_program = self.var_program.get()
        subjects = MMU_COURSES[selected_program][selected_trimester]
        self.var_subject.configure(values=subjects)
        if subjects:
            self.var_subject.set(subjects[0])
        else:
            self.var_subject.set("No Subjects Available")

    def open_timer(self):
        selected_subject = self.var_subject.get()
        if selected_subject and selected_subject != "No Subjects Available":
            FocusTimerWindow(self, selected_subject, self.receive_timer_data)

    def receive_timer_data(self, subject, duration, confidence):
        self._save_to_memory_and_switch(subject, duration, confidence)

    def save_session(self):
        subject = self.var_subject.get()
        duration = int(self.var_duration.get())
        confidence = int(self.var_confidence.get())
        self._save_to_memory_and_switch(subject, duration, confidence)

    def _save_to_memory_and_switch(self, subject, duration, confidence):
        if subject not in self.mock_database:
            self.mock_database[subject] = {"old_score": 80.0} 
            
        self.mock_database[subject]["duration"] = duration
        self.mock_database[subject]["confidence"] = confidence
        self.mock_database[subject]["days_ago"] = 0 
        
        self.subject_list = list(self.mock_database.keys())
        self.analytics_dropdown.configure(values=self.subject_list)
        
        self.show_page("analytics")
        self.analytics_dropdown.set(subject)
        self.refresh_analytics(subject)

    # ------------------------------------------
    # PAGE 3: ANALYTICS & INSIGHTS
    # ------------------------------------------
    def build_analytics_page(self):
        self.filter_frame = ctk.CTkFrame(self.analytics_page, fg_color="transparent")
        self.filter_frame.pack(pady=(20, 10), fill="x", padx=40)
        
        ctk.CTkLabel(self.filter_frame, text="Viewing Analytics For:", font=("Helvetica", 16)).pack(side="left", padx=(0, 10))
        
        self.analytics_dropdown = ctk.CTkOptionMenu(self.filter_frame, values=self.subject_list, width=300, command=self.refresh_analytics)
        self.analytics_dropdown.pack(side="left")

        self.textbox_insights = ctk.CTkTextbox(self.analytics_page, height=140, font=("Helvetica", 14), fg_color="#2b2b2b")
        self.textbox_insights.pack(fill="x", padx=40, pady=10)

        self.chart_frame = ctk.CTkFrame(self.analytics_page, fg_color="#1e1e1e")
        self.chart_frame.pack(fill="both", expand=True, padx=40, pady=10)
        self.canvas_widget = None 

    def refresh_analytics(self, selected_subject):
        data = self.mock_database[selected_subject]
        
        fake_date_str = (datetime.now() - timedelta(days=data["days_ago"])).strftime("%Y-%m-%d")
        new_score, penalty = calculate_time_decay(data["old_score"], fake_date_str)
        
        insights_text = get_algorithmic_insights(data["duration"], data["confidence"], penalty)
        self.textbox_insights.configure(state="normal")
        self.textbox_insights.delete("0.0", "end")
        self.textbox_insights.insert("0.0", f"--- SYSTEM EVALUATION ---\n\n{insights_text}")
        self.textbox_insights.configure(state="disabled")

        self.draw_chart(data["old_score"], new_score, penalty)

    def draw_chart(self, old_score, new_score, penalty):
        if self.canvas_widget:
            self.canvas_widget.destroy()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), facecolor='#1e1e1e')
        fig.patch.set_facecolor('#1e1e1e')

        ax1.set_facecolor('#1e1e1e')
        bars = ax1.bar(['Original', 'Decayed'], [old_score, new_score], color=['#3498db', '#e74c3c' if penalty > 0 else '#2ecc71'], width=0.5)
        ax1.set_ylim(0, 100)
        ax1.tick_params(colors='white')
        ax1.set_title("Penalty Impact", color='white')
        for spine in ax1.spines.values(): spine.set_color('#444444')
        for bar in bars: ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f"{bar.get_height()}%", ha='center', color='white', fontweight='bold')

        ax2.set_facecolor('#1e1e1e')
        future_days = np.array([0, 7, 14, 21, 28])
        future_scores = np.maximum(new_score - (future_days / 7) * 5.0, 0)
        ax2.plot(future_days, future_scores, color='#e67e22', marker='o', linewidth=2)
        ax2.set_ylim(0, 100)
        ax2.tick_params(colors='white')
        ax2.set_title("30-Day Forgetting Curve", color='white')
        for spine in ax2.spines.values(): spine.set_color('#444444')

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = NexusApp()
    app.mainloop()