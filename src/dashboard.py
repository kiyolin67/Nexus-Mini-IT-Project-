import os
import customtkinter as ctk
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai

 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calculate_time_decay(current_score, last_studied_date_str):
    if not last_studied_date_str:
        return current_score, 0.0

    last_studied = datetime.strptime(last_studied_date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    days_passed = (today - last_studied).days

    if days_passed > 7:
        weeks_missed = days_passed // 7
        penalty = weeks_missed * 5.0
        new_score = max(current_score - penalty, 0.0)
        return round(new_score, 1), penalty

    return current_score, 0.0

def get_ai_study_advice(topic_name, duration_mins, confidence_level):
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert study advisor for foundation university students. 
        A student has just studied '{topic_name}' for {duration_mins} minutes and rates their confidence level as {confidence_level}/5.

        Provide exactly 2-3 short sentences of actionable, scientific study advice based on this data.
        If they studied over 90 minutes, warn them about cognitive burnout.
        Do not use formatting like bolding or bullet points.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    
    except Exception as e:
        print(f"API Error Found: {e}")
        return "Insights offline. Please try again later. Remember to use Spaced Repetition and take a 15-minute break every hour!"

# ==========================================
# 2. CUSTOMTKINTER DASHBOARD
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class NexusDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexus - Study Session Analyzer")
        self.geometry("900x600")
        self.configure(fg_color="#1e1e1e") # Dark Gray Theme

        # Create Left Frame (Inputs)
        self.left_frame = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="#2b2b2b")
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.setup_input_ui()
        self.setup_output_ui()

    def setup_input_ui(self):
        ctk.CTkLabel(self.left_frame, text="Session Data", font=("Helvetica", 20, "bold")).pack(pady=(20, 10))

        # Topic Input
        self.entry_topic = ctk.CTkEntry(self.left_frame, placeholder_text="Topic (e.g., Calculus)", width=250)
        self.entry_topic.pack(pady=10)

        # Duration Input
        self.entry_duration = ctk.CTkEntry(self.left_frame, placeholder_text="Duration (mins)", width=250)
        self.entry_duration.pack(pady=10)

        # Confidence Slider
        ctk.CTkLabel(self.left_frame, text="Confidence Level (1-5)").pack(pady=(10, 0))
        self.slider_confidence = ctk.CTkSlider(self.left_frame, from_=1, to=5, number_of_steps=4, width=250)
        self.slider_confidence.set(3)
        self.slider_confidence.pack(pady=5)

        # Current Mastery Score
        self.entry_score = ctk.CTkEntry(self.left_frame, placeholder_text="Current Score (0-100)", width=250)
        self.entry_score.pack(pady=10)

        # Days Ago Input (Easier for UI testing than typing dates)
        self.entry_days = ctk.CTkEntry(self.left_frame, placeholder_text="Days Since Last Studied", width=250)
        self.entry_days.pack(pady=10)

        # Analyze Button
        self.btn_analyze = ctk.CTkButton(self.left_frame, text="Analyze Session", command=self.run_analysis, fg_color="#4CAF50", hover_color="#45a049")
        self.btn_analyze.pack(pady=30)

    def setup_output_ui(self):
        # AI Text Box
        ctk.CTkLabel(self.right_frame, text="Nexus AI Insight", font=("Helvetica", 16, "bold")).pack(pady=(10, 5))
        self.textbox_ai = ctk.CTkTextbox(self.right_frame, height=100, font=("Helvetica", 14), fg_color="#2b2b2b")
        self.textbox_ai.pack(fill="x", padx=20, pady=5)
        self.textbox_ai.insert("0.0", "Enter your data on the left to generate insights...")
        self.textbox_ai.configure(state="disabled")

        # Frame to hold the Matplotlib Chart
        self.chart_frame = ctk.CTkFrame(self.right_frame, fg_color="#1e1e1e")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.canvas_widget = None # Will hold the drawn graph

    def run_analysis(self):
        # 1. Gather Data from UI
        topic = self.entry_topic.get() or "General Study"
        duration = int(self.entry_duration.get() or 0)
        confidence = int(self.slider_confidence.get())
        original_score = float(self.entry_score.get() or 85.0)
        days_ago = int(self.entry_days.get() or 0)

        # 2. Convert "Days Ago" into a fake date string for your backend function
        fake_date_str = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        # 3. Run Backend Math & AI
        new_score, penalty = calculate_time_decay(original_score, fake_date_str)
        
        self.btn_analyze.configure(text="Generating...", state="disabled")
        self.update() # Force UI refresh
        
        ai_advice = get_ai_study_advice(topic, duration, confidence)

        # 4. Update UI Text
        self.textbox_ai.configure(state="normal")
        self.textbox_ai.delete("0.0", "end")
        self.textbox_ai.insert("0.0", ai_advice)
        self.textbox_ai.configure(state="disabled")

        self.btn_analyze.configure(text="Analyze Session", state="normal")

        # 5. Draw the Matplotlib Bar Chart
        self.draw_chart(original_score, new_score, penalty)

    def draw_chart(self, old_score, new_score, penalty):
        # Clear the old chart if one exists
        if self.canvas_widget:
            self.canvas_widget.destroy()

        
        fig, ax = plt.subplots(figsize=(5, 3), facecolor='#1e1e1e')
        ax.set_facecolor('#1e1e1e')

        # Data
        labels = ['Original Score', 'Decayed Score']
        values = [old_score, new_score]
        colors = ['#3498db', '#e74c3c' if penalty > 0 else '#2ecc71']

        # Bar Chart
        bars = ax.bar(labels, values, color=colors, width=0.5)
        ax.set_ylim(0, 100)
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('#444444')
            
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval}%", ha='center', color='white', fontweight='bold')

        # Embed into CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = NexusDashboard()
    app.mainloop()