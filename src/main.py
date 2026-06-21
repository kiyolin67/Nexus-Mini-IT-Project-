import customtkinter as ctk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- MODULE IMPORTS ---
from timer import FocusTimerWindow
import database as db
# from heatmap_ui import ActivityHeatmap migth remove features
from xp_dashboard import RPGDashboard
# from database import save_focus_session, set_current_user hardcoded 

# set_current_user("Lin") # HARDCODED FOR NOW, WILL IMPLEMENT PROPER LOGIN SYSTEM LATER

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

def get_grade(score):
    """Converts a mastery percentage into a standard University Letter Grade."""
    if score >= 80: return "A", "#2ecc71"  # Green
    if score >= 70: return "B", "#3498db"  # Blue
    if score >= 60: return "C", "#f1c40f"  # Yellow
    if score >= 50: return "D", "#e67e22"  # Orange
    return "F", "#e74c3c"                  # Red

def get_algorithmic_insights(duration_mins, confidence_level, penalty):
    """Now returns a list of dictionaries containing both text AND a hex color code."""
    insights = []
    
    # Decay Insights
    if penalty >= 10.0:
        insights.append({"text": "🚨 CRITICAL DECAY: High memory loss detected. Immediate review required.", "color": "#e74c3c"})
    elif penalty > 0.0:
        insights.append({"text": "⚠️ WARNING: Memory decay has started. Schedule a review session.", "color": "#f1c40f"})
    else:
        insights.append({"text": "✅ OPTIMAL: You are studying within the ideal spaced-repetition window.", "color": "#2ecc71"})

    # Efficiency Insights
    if duration_mins > 90:
        insights.append({"text": "🧠 EFFICIENCY DROP: Sessions over 90 mins risk cognitive burnout. Take breaks.", "color": "#e67e22"})
    elif duration_mins < 20:
        insights.append({"text": "⏱️ MICRO-SESSION: Too short for deep cognitive work. Aim for 25+ mins.", "color": "#f1c40f"})

    # Strategy Insights
    if confidence_level <= 2:
        insights.append({"text": "📚 STRATEGY: Low confidence. Shift focus from passive reading to active recall.", "color": "#3498db"})
    elif confidence_level >= 4:
        insights.append({"text": "🚀 MASTERY: High confidence. Begin testing yourself with past year exam papers.", "color": "#2ecc71"})

    return insights 

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
        self.geometry("1100x850")

        self.mock_database = {}  # mock databse for testing
        self.subject_list = []
        self.sync_cloud_database()
        

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

        self.show_page("home")

    def sync_cloud_database(self):
        import database as db
        user_sessions = db.get_user_sessions(db.CURRENT_USER)
        self.mock_database = {}
        self.subject_list = []
        if not user_sessions:
            print(f"No existing sessions found for {db.CURRENT_USER}")
            self.mock_database["Welcome"] = {"old_score": 100, "days_ago": 0, "duration": 0, "confidence": 10, "friction_tags": []}
            self.subject_list.append("Welcome")
            return

        print(f"Found {len(user_sessions)} sessions in cloud. Compiling...")
        
        for row in user_sessions:
            topic = row[2]
            duration = row[3]
            confidence = row[4]
            friction_tag = row[5]
            date_logged = row[6]

            # Calculate days ago based on the cloud timestamp
            from datetime import datetime, date
            if isinstance(date_logged, str):
                try:
                    date_obj = datetime.strptime(date_logged, "%Y-%m-%d").date()
                except ValueError:
                    date_obj = date.today()
            else:
                date_obj = date_logged
                
            days_ago = (date.today() - date_obj).days

            # Math to convert 1-10 confidence into a standard 100% test score
            calculated_score = int((confidence / 10) * 100)

            # If this is the first time seeing this topic, create its dictionary
            if topic not in self.mock_database:
                self.mock_database[topic] = {
                    "old_score": calculated_score,
                    "days_ago": days_ago,
                    "duration": duration,
                    "confidence": confidence,
                    "friction_tags": [friction_tag] if friction_tag else []
                }
                self.subject_list.append(topic)
            else:
                # update it with the newest data
                self.mock_database[topic]["old_score"] = calculated_score
                self.mock_database[topic]["days_ago"] = days_ago
                self.mock_database[topic]["duration"] += duration
                self.mock_database[topic]["confidence"] = confidence
                if friction_tag:
                    self.mock_database[topic]["friction_tags"].append(friction_tag)
                                                                      
    def refresh_analytics(self, selected_subject):
        if selected_subject == "Welcome":
            self.lbl_score_text.configure(text="Welcome to Nexus Analytics")
            self.lbl_grade.configure(text="Awaiting Data...", text_color="gray")

            for widget in self.insights_container.winfo_children():
                widget.destroy()
            
            ctk.CTkLabel(self.insights_container, text="Head Over to 'Log Study Sessions To Start", font=("Helvetica", 14), text_color="silver"
            ).pack(pady=40)
            if self.canvas_widget:
                self.canvas_widget.destroy()
                self.canvas_widget = None
            return
        
        data = self.mock_database[selected_subject]
        
        fake_date_str = (datetime.now() - timedelta(days=data["days_ago"])).strftime("%Y-%m-%d")
        new_score, penalty = calculate_time_decay(data["old_score"], fake_date_str)
        
        # --- SCORE & GRADE UI ---
        grade_letter, grade_color = get_grade(new_score)
        self.lbl_grade.configure(text=f"{new_score}% (Grade: {grade_letter})", text_color=grade_color)

        # --- INSIGHTS UI ---
        for widget in self.insights_container.winfo_children():
            widget.destroy()

        # friction insight
        tags = data.get("friction_tags", [])
        if tags:
            latest_tag = tags[-1]
            tag_count = tags.count(latest_tag)

            friction_card = ctk.CTkFrame(self.insights_container, fg_color="#e74c3c", corner_radius=5, border_width =1, border_color="#c0392b")
            friction_card.pack(fill="x", pady=(0,10))
            tag_msg = f"🛑 DIAGNOSTIC: You've tagged '{latest_tag}' {tag_count} time(s) for this subject. Stop pushing blindly and address this specific roadblock."
            ctk.CTkLabel(friction_card, text=tag_msg, text_color="#e67e22", font=("Helvetica", 14, "bold"), justify="left", wraplength=700).pack(side="left", padx=15, pady=10)
       
       
        insights_data = get_algorithmic_insights(data["duration"], data["confidence"], penalty)
        
        for insight in insights_data:
            card = ctk.CTkFrame(self.insights_container, fg_color="#2b2b2b", corner_radius=5)
            card.pack(fill="x", pady=3)
            
            # The colored text
            ctk.CTkLabel(card, text=insight["text"], text_color=insight["color"], font=("Helvetica", 14, "bold"), justify="left").pack(side="left", padx=10, pady=5)

        # --- UPDATE CHARTS ---
        self.draw_chart(data["old_score"], new_score, penalty)

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
        # --- DYNAMIC DATA CALCULATIONS ---
        # 1. Total Study Hours
        total_minutes = sum(data.get("duration", 0) for data in self.mock_database.values())
        total_hours = round(total_minutes / 60, 1)

        # 2. Subjects Tracked
        active_subjects = [sub for sub in self.subject_list if sub != "Welcome"]
        total_subjects = len(active_subjects)

        # 3. Gamification Stats
        total_xp = total_minutes * 10  # 10 XP per minute studied
        
        # Calculate today's minutes
        today_mins = sum(data.get("duration", 0) for data in self.mock_database.values() if data.get("days_ago", -1) == 0)

        # 4. Current Streak (Simplified: 1 if studied today, else 0)
        streak = 1 if today_mins > 0 else 0
        
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
        ctk.CTkLabel(card1, text=f"{total_hours} hrs", font=("Helvetica", 28, "bold"), text_color="#3498db").pack()

        # Metric 2: Current Streak
        card2 = ctk.CTkFrame(metrics_frame, fg_color="#2b2b2b", corner_radius=15, width=200, height=100)
        card2.pack(side="left", expand=True, padx=10)
        card2.pack_propagate(False)
        ctk.CTkLabel(card2, text="Current Streak", font=("Helvetica", 14), text_color="gray").pack(pady=(15, 5))
        ctk.CTkLabel(card2, text=f"{streak} Days 🔥", font=("Helvetica", 28, "bold"), text_color="#e67e22").pack()

        # Metric 3: Subjects Tracked
        card3 = ctk.CTkFrame(metrics_frame, fg_color="#2b2b2b", corner_radius=15, width=200, height=100)
        card3.pack(side="left", expand=True, padx=10)
        card3.pack_propagate(False)
        ctk.CTkLabel(card3, text="Subjects Tracked", font=("Helvetica", 14), text_color="gray").pack(pady=(15, 5))
        ctk.CTkLabel(card3, text=f"{total_subjects}", font=("Helvetica", 28, "bold"), text_color="#2ecc71").pack()

        # XP DASHBOARD MENU 
        ctk.CTkLabel(self.home_page, text="Progression Dashboard", font=("Helvetica", 18, "bold")).pack(pady=(40, 10))
        
        self.rpg_widget = RPGDashboard(self.home_page, daily_mins_studied=today_mins, daily_goal=120, total_xp=total_xp)
        self.rpg_widget.pack(pady=10, padx=50, fill="x")

        # CHECKLIST 

        ctk.CTkLabel(self.home_page, text="Action Items & Deadlines", font=("Helvetica", 18, "bold")).pack(pady=(30, 10))

        self.deadline_frame = ctk.CTkScrollableFrame(self.home_page, fg_color="transparent", height=150)
        self.deadline_frame.pack(pady=0, padx=50, fill="x")

        # 1. Fetch real data from your Aiven database
        real_deadlines = db.get_user_deadlines(db.CURRENT_USER)

        # 2. Handle the Empty State gracefully
        if not real_deadlines:
             ctk.CTkLabel(self.deadline_frame, text="No upcoming deadlines found in database. You're all caught up!", font=("Helvetica", 14), text_color="gray").pack(pady=30)
        else:
            # 3. Dynamically build the UI from the database rows
            for row in real_deadlines:
                task_name = row[0]
                due_date = row[1]
                is_urgent = bool(row[2]) # Converts MySQL's 1 or 0 into True or False

                card = ctk.CTkFrame(self.deadline_frame, fg_color="#2b2b2b", corner_radius=8)
                card.pack(fill="x", pady=5, padx=5)
                
                cb = ctk.CTkCheckBox(
                    card, 
                    text=task_name, 
                    font=("Helvetica", 14), 
                    text_color="white", 
                    fg_color="#2ecc71", 
                    hover_color="#27ae60", 
                    checkbox_height=20, 
                    checkbox_width=20
                )
                cb.pack(side="left", padx=15, pady=10)
                
                date_color = "#e74c3c" if is_urgent else "gray"
                ctk.CTkLabel(card, text=due_date, font=("Helvetica", 12, "bold"), text_color=date_color).pack(side="right", padx=15)
    # ------------------------------------------
    # PAGE 2: DATA ENTRY 
    # ------------------------------------------
    def build_input_page(self):
        # 1. Page Header (More breathing room)
        ctk.CTkLabel(self.input_page, text="Log Study Session", font=("Helvetica", 36, "bold")).pack(pady=(40, 20))

        # 2. The "Form Card" 
        form_card = ctk.CTkFrame(self.input_page, fg_color="#2b2b2b", corner_radius=15)
        form_card.pack(pady=10, padx=50, fill="x")

        # Container for the dropdowns to center them inside the card
        dropdown_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        dropdown_frame.pack(pady=30)
        ctk.CTkLabel(dropdown_frame, text="Program:", font=("Helvetica", 16)).grid(row=0, column=0, padx=20, pady=10, sticky="e")
        programs = list(MMU_COURSES.keys())
        self.var_program = ctk.CTkOptionMenu(dropdown_frame, values=programs, width=500, height=40, font=("Helvetica", 14), command=self.update_trimesters)
        self.var_program.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(dropdown_frame, text="Trimester:", font=("Helvetica", 16)).grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.var_trimester = ctk.CTkOptionMenu(dropdown_frame, values=[], width=500, height=40, font=("Helvetica", 14), command=self.update_subjects)
        self.var_trimester.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(dropdown_frame, text="Subject:", font=("Helvetica", 16)).grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.var_subject = ctk.CTkOptionMenu(dropdown_frame, values=[], width=500, height=40, font=("Helvetica", 14))
        self.var_subject.grid(row=2, column=1, padx=10, pady=10)

        self.var_program.set(programs[0])
        self.update_trimesters(programs[0])

        self.log_tabs = ctk.CTkTabview(self.input_page, width=700, height=500)
        self.log_tabs.pack(pady=(20, 40))
        
        self.log_tabs.add("⏱️ Active Timer")
        self.log_tabs.add("📝 Manual Entry")

        # Active Timer Tab
        ctk.CTkLabel(self.log_tabs.tab("⏱️ Active Timer"), text="Study with the app open to track exact time.", font=("Helvetica", 16), text_color="gray").pack(pady=(40, 20))
        ctk.CTkButton(self.log_tabs.tab("⏱️ Active Timer"), text="Launch Focus Timer", height=60, width=300, font=("Helvetica", 18, "bold"), fg_color="#3498db", hover_color="#2980b9", command=self.open_timer).pack(pady=20)

        # Manual Entry Tab
        # ----------------------------------------
        # Manual Entry Tab (SCROLLABLE UPGRADE)
        # ----------------------------------------
        self.manual_container = ctk.CTkScrollableFrame(self.log_tabs.tab("📝 Manual Entry"), fg_color="transparent")
        self.manual_container.pack(fill="both", expand=True)

        ctk.CTkLabel(self.manual_container, text="Duration (Minutes):", font=("Helvetica", 16)).pack(pady=(10, 5))
        self.var_duration = ctk.CTkSlider(self.manual_container, from_=10, to=180, number_of_steps=34, width=400)
        self.var_duration.set(60)
        self.var_duration.pack(pady=10)
        
        self.label_duration_val = ctk.CTkLabel(self.manual_container, text="60 mins", text_color="#3498db", font=("Helvetica", 16, "bold"))
        self.label_duration_val.pack()
        self.var_duration.configure(command=lambda val: self.label_duration_val.configure(text=f"{int(val)} mins"))

        ctk.CTkLabel(self.manual_container, text="Confidence Level (1-5):", font=("Helvetica", 16)).pack(pady=(20, 5))
        
        self.var_confidence = ctk.CTkSlider(self.manual_container, from_=1, to=5, number_of_steps=4, width=400, command=self.on_confidence_change)
        self.var_confidence.set(3)
        self.var_confidence.pack(pady=10)

        self.label_conf_val = ctk.CTkLabel(self.manual_container, text="Level 3", text_color="#3498db", font=("Helvetica", 16, "bold"))
        self.label_conf_val.pack()

        # Friction UI
        self.friction_frame = ctk.CTkFrame(self.manual_container, fg_color="transparent")        
        ctk.CTkLabel(self.friction_frame, text="What was your primary roadblock?", text_color="#e74c3c", font=("Helvetica", 14, "bold")).pack(pady=(15, 5))
        self.var_friction = ctk.CTkOptionMenu(
            self.friction_frame, 
            values=["Forgot Prerequisite", "Burnout/Fatigue", "Material Too Complex", "Poor Time Management"], 
            width=300, 
            fg_color="#c0392b", 
            button_color="#e74c3c", 
            button_hover_color="#c0392b"
        )
        self.var_friction.pack()
        
        self.btn_save = ctk.CTkButton(self.manual_container, text="Save Manual Log", height=45, width=250, font=("Helvetica", 16, "bold"), fg_color="#2ecc71", hover_color="#27ae60", command=self.save_session)
        self.btn_save.pack(pady=(20, 10))
    
    def on_confidence_change(self, val):
        conf = int(val)
        self.lavel_conf_val.configure(text=f"Level {conf}")
        
        if conf <= 2:
            self.friction_frame.pack(before=self.btn_save, pady=10)
        else:
            self.friction_frame.pack_forget()

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
        # save_focus_session(subject, duration, confidence) # HARDCODED

        self._save_to_memory_and_switch(
            subject,
            duration,
            confidence
        )

    def save_session(self):
        subject = self.var_subject.get()
        duration = int(self.var_duration.get())
        confidence = int(self.var_confidence.get())
        friction_tag = self.var_friction.get() if confidence <= 2 else None
        self._save_to_memory_and_switch(subject, duration, confidence, friction_tag)

        # save_focus_session(subject, duration, confidence) # HARDCODED

    def _save_to_memory_and_switch(self, subject, duration, confidence, friction_tag=None):
        if subject not in self.mock_database:
            self.mock_database[subject] = {"old_score": 80.0} 
            
        self.mock_database[subject]["duration"] = duration
        self.mock_database[subject]["confidence"] = confidence
        self.mock_database[subject]["days_ago"] = 0

        if "friction_tags" not in self.mock_database[subject]:
            self.mock_database[subject]["friction_tags"] = []
        
        if friction_tag:
            self.mock_database[subject]["friction_tags"].append(friction_tag)   
        
        self.subject_list = list(self.mock_database.keys())
        self.analytics_dropdown.configure(values=self.subject_list)
        
        self.show_page("analytics")
        self.analytics_dropdown.set(subject)
        self.refresh_analytics(subject)

# ------------------------------------------
    # PAGE 3: ANALYTICS & INSIGHTS (UPGRADED)
    # ------------------------------------------
    def build_analytics_page(self):
        # 1. Filter Area (Upgraded)
        self.filter_frame = ctk.CTkFrame(self.analytics_page, fg_color="transparent")
        self.filter_frame.pack(pady=(30, 20), fill="x", padx=40)
        ctk.CTkLabel(self.filter_frame, text="Subject:", font=("Helvetica", 20, "bold"), text_color="gray").pack(side="left", padx=(0, 15))
        
        # Make the dropdown massive and bold so it feels like a title
        self.analytics_dropdown = ctk.CTkOptionMenu(
            self.filter_frame, 
            values=self.subject_list, 
            width=400, 
            height=45, 
            font=("Helvetica", 18, "bold"),
            dropdown_font=("Helvetica", 14),
            command=self.refresh_analytics
        )
        self.analytics_dropdown.pack(side="left")

        # 2. Big Mastery Score & Grade Display
        self.score_display_frame = ctk.CTkFrame(self.analytics_page, fg_color="#2b2b2b", corner_radius=10)
        self.score_display_frame.pack(fill="x", padx=40, pady=10)
        
        self.lbl_score_text = ctk.CTkLabel(self.score_display_frame, text="Current Mastery Score:", font=("Helvetica", 18))
        self.lbl_score_text.pack(side="left", padx=20, pady=15)
        
        self.lbl_grade = ctk.CTkLabel(self.score_display_frame, text="85% (Grade: A)", font=("Helvetica", 24, "bold"), text_color="#2ecc71")
        self.lbl_grade.pack(side="right", padx=20, pady=15)

        # 3. Dynamic Insights Container
        self.insights_container = ctk.CTkScrollableFrame(self.analytics_page, height=120, fg_color="#1e1e1e")
        self.insights_container.pack(fill="x", padx=40, pady=5, expand=False)

        # 4. Chart Area
        self.chart_frame = ctk.CTkFrame(self.analytics_page, fg_color="#1e1e1e")
        self.chart_frame.pack(fill="both", expand=True, padx=40, pady=10)
        self.canvas_widget = None 

    def draw_chart(self, old_score, new_score, penalty):
        if self.canvas_widget:
            self.canvas_widget.destroy()

        plt.close('all') 
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), facecolor="#1e1e1e")
        fig.patch.set_facecolor('#1e1e1e')

        # Bar Chart (Upgraded)
        ax1.set_facecolor('#1e1e1e')
        bars = ax1.bar(['Peak Mastery', 'Current Recall'], [old_score, new_score], color=['#3498db', '#e74c3c' if penalty > 0 else '#2ecc71'], width=0.5)
        ax1.set_ylim(0, 100)
        ax1.tick_params(colors='white')
        ax1.set_title("Current Memory Retention", color='white', pad=15, fontsize=12, fontweight='bold')
        for spine in ax1.spines.values(): spine.set_color('#444444')
        for bar in bars: ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f"{bar.get_height()}%", ha='center', color='white', fontweight='bold')

        # Line Graph (Upgraded)
        ax2.set_facecolor('#1e1e1e')
        future_days = np.array([0, 7, 14, 21, 28])
        future_scores = np.maximum(new_score - (future_days / 7) * 5.0, 0)
        
        # Add the red "Danger Zone" threshold line
        ax2.axhline(y=60, color='#e74c3c', linestyle='--', alpha=0.5, linewidth=2)
        ax2.text(2, 62, "Failing Threshold", color='#e74c3c', fontsize=9, alpha=0.8)

        ax2.plot(future_days, future_scores, color='#e67e22', marker='o', linewidth=3, markersize=8)
        ax2.set_ylim(0, 100)
        ax2.tick_params(colors='white')
        ax2.set_title("Projected Forgetting Curve", color='white', pad=15, fontsize=12, fontweight='bold')
        ax2.set_xlabel("Days from Today", color='gray', fontsize=10)
        for spine in ax2.spines.values(): spine.set_color('#444444')

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = NexusApp()
    app.mainloop()

