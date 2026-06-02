import customtkinter as ctk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
# 2. THE MULTI-PAGE APPLICATION
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class NexusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexus - Student Operating System")
        self.geometry("1100x700")

        # MOCK DATABASE: Simulating Samuel's SQL backend for multiple subjects
        self.mock_database = {
            "FOE1010 - Calculus": {"duration": 60, "confidence": 4, "old_score": 85.0, "days_ago": 8},
            "FCI1020 - Intro to Programming": {"duration": 120, "confidence": 2, "old_score": 60.0, "days_ago": 15},
            "FOB1030 - Business Mgmt": {"duration": 30, "confidence": 5, "old_score": 95.0, "days_ago": 2}
        }
        self.subject_list = list(self.mock_database.keys())

        # Setup Grid Layout 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- NAVIGATION SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar_frame, text="NEXUS", font=("Helvetica", 28, "bold"), text_color="#3498db").pack(pady=(30, 40))

        self.btn_nav_input = ctk.CTkButton(self.sidebar_frame, text="Log Study Session", command=lambda: self.show_page("input"), fg_color="transparent", border_width=1, hover_color="#2c3e50")
        self.btn_nav_input.pack(pady=10, padx=20, fill="x")

        self.btn_nav_analytics = ctk.CTkButton(self.sidebar_frame, text="View Analytics", command=lambda: self.show_page("analytics"), fg_color="transparent", border_width=1, hover_color="#2c3e50")
        self.btn_nav_analytics.pack(pady=10, padx=20, fill="x")

        # --- PAGE CONTAINERS ---
        self.input_page = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")
        self.analytics_page = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")

        self.build_input_page()
        self.build_analytics_page()

        self.show_page("input")

    def show_page(self, page_name):
        self.input_page.grid_forget()
        self.analytics_page.grid_forget()

        if page_name == "input":
            self.input_page.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif page_name == "analytics":
            self.analytics_page.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            # Default to the first subject in the list when opening the page
            self.analytics_dropdown.set(self.subject_list[0])
            self.refresh_analytics(self.subject_list[0]) 

    # ------------------------------------------
    # PAGE 1: DATA ENTRY 
    # ------------------------------------------
    def build_input_page(self):
        ctk.CTkLabel(self.input_page, text="Log New Session", font=("Helvetica", 32, "bold")).pack(pady=(40, 20))

        ctk.CTkLabel(self.input_page, text="Select Subject:", font=("Helvetica", 16)).pack(pady=(20, 5))
        self.var_subject = ctk.CTkOptionMenu(self.input_page, values=self.subject_list, width=300, height=40)
        self.var_subject.pack(pady=5)

        ctk.CTkLabel(self.input_page, text="Study Duration (Minutes):", font=("Helvetica", 16)).pack(pady=(30, 5))
        self.var_duration = ctk.CTkSlider(self.input_page, from_=10, to=180, number_of_steps=34, width=400)
        self.var_duration.set(60)
        self.var_duration.pack(pady=5)
        
        self.label_duration_val = ctk.CTkLabel(self.input_page, text="60 mins", text_color="#3498db", font=("Helvetica", 14, "bold"))
        self.label_duration_val.pack()
        self.var_duration.configure(command=lambda val: self.label_duration_val.configure(text=f"{int(val)} mins"))

        ctk.CTkLabel(self.input_page, text="Confidence Level (1-5):", font=("Helvetica", 16)).pack(pady=(30, 5))
        self.var_confidence = ctk.CTkSlider(self.input_page, from_=1, to=5, number_of_steps=4, width=400)
        self.var_confidence.set(3)
        self.var_confidence.pack(pady=5)

        self.label_conf_val = ctk.CTkLabel(self.input_page, text="Level 3", text_color="#3498db", font=("Helvetica", 14, "bold"))
        self.label_conf_val.pack()
        self.var_confidence.configure(command=lambda val: self.label_conf_val.configure(text=f"Level {int(val)}"))

        ctk.CTkButton(self.input_page, text="Save & Analyze", height=50, width=200, fg_color="#2ecc71", hover_color="#27ae60", command=self.save_session).pack(pady=50)

    def save_session(self):
        """Updates the mock DB with the newly logged data, then switches to Analytics."""
        subject = self.var_subject.get()
        
        # Update the dictionary (simulating a database UPDATE)
        self.mock_database[subject]["duration"] = int(self.var_duration.get())
        self.mock_database[subject]["confidence"] = int(self.var_confidence.get())
        self.mock_database[subject]["days_ago"] = 0 # Just studied today!
        
        # Switch to analytics and force it to show the subject just logged
        self.show_page("analytics")
        self.analytics_dropdown.set(subject)
        self.refresh_analytics(subject)

    # ------------------------------------------
    # PAGE 2: ANALYTICS & INSIGHTS (Upgraded)
    # ------------------------------------------
    def build_analytics_page(self):
        # NEW: Filter Area at the top
        self.filter_frame = ctk.CTkFrame(self.analytics_page, fg_color="transparent")
        self.filter_frame.pack(pady=(20, 10), fill="x", padx=40)
        
        ctk.CTkLabel(self.filter_frame, text="Viewing Analytics For:", font=("Helvetica", 16)).pack(side="left", padx=(0, 10))
        
        # The dynamic dropdown that triggers refresh_analytics whenever it is changed
        self.analytics_dropdown = ctk.CTkOptionMenu(self.filter_frame, values=self.subject_list, width=250, command=self.refresh_analytics)
        self.analytics_dropdown.pack(side="left")

        # Insights Panel
        self.textbox_insights = ctk.CTkTextbox(self.analytics_page, height=140, font=("Helvetica", 14), fg_color="#2b2b2b")
        self.textbox_insights.pack(fill="x", padx=40, pady=10)

        # Graph Area
        self.chart_frame = ctk.CTkFrame(self.analytics_page, fg_color="#1e1e1e")
        self.chart_frame.pack(fill="both", expand=True, padx=40, pady=10)
        self.canvas_widget = None 

    def refresh_analytics(self, selected_subject):
        """Pulls data for the selected subject and redraws the UI."""
        
        # 1. Fetch data for this specific subject from mock DB
        data = self.mock_database[selected_subject]
        
        # 2. Math Engine
        fake_date_str = (datetime.now() - timedelta(days=data["days_ago"])).strftime("%Y-%m-%d")
        new_score, penalty = calculate_time_decay(data["old_score"], fake_date_str)
        
        # 3. Insights Engine
        insights_text = get_algorithmic_insights(data["duration"], data["confidence"], penalty)
        self.textbox_insights.configure(state="normal")
        self.textbox_insights.delete("0.0", "end")
        self.textbox_insights.insert("0.0", f"--- SYSTEM EVALUATION ---\n\n{insights_text}")
        self.textbox_insights.configure(state="disabled")

        # 4. Draw Charts
        self.draw_chart(data["old_score"], new_score, penalty)

    def draw_chart(self, old_score, new_score, penalty):
        if self.canvas_widget:
            self.canvas_widget.destroy()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), facecolor='#1e1e1e')
        fig.patch.set_facecolor('#1e1e1e')

        # Bar Chart
        ax1.set_facecolor('#1e1e1e')
        bars = ax1.bar(['Original', 'Decayed'], [old_score, new_score], color=['#3498db', '#e74c3c' if penalty > 0 else '#2ecc71'], width=0.5)
        ax1.set_ylim(0, 100)
        ax1.tick_params(colors='white')
        ax1.set_title("Penalty Impact", color='white')
        for spine in ax1.spines.values(): spine.set_color('#444444')
        for bar in bars: ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f"{bar.get_height()}%", ha='center', color='white', fontweight='bold')

        # Line Graph
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