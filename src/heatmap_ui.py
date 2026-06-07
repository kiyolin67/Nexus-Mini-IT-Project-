import customtkinter as ctk
from datetime import datetime, timedelta
import random

class ActivityHeatmap(ctk.CTkFrame):
    """
    MODULE 3: The Data Science Activity Tracker
    A GitHub-style contribution calendar built natively in CustomTkinter.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="#2b2b2b", corner_radius=15)
        
        # Simulate 35 days of study data (5 weeks)
        self.mock_history = self.generate_mock_data()

        self.setup_ui()

    def generate_mock_data(self):
        """Generates random study durations (0 to 150 mins) to make the graph look alive."""
        data = []
        for _ in range(35):
            # 40% chance the student didn't study that day, otherwise random minutes
            if random.random() < 0.4:
                data.append(0)
            else:
                data.append(random.randint(15, 150))
        return data

    def get_color_for_duration(self, minutes):
        """Threshold logic to determine the square's color based on study time."""
        if minutes == 0:
            return "#1e1e1e"  # Dark gray (No activity)
        elif minutes < 30:
            return "#0e4429"  # Very dark green (Micro-session)
        elif minutes < 60:
            return "#006d32"  # Dark green (Standard session)
        elif minutes < 100:
            return "#26a641"  # Bright green (Solid session)
        else:
            return "#39d353"  # Neon green (Deep work / Mastery)

    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        ctk.CTkLabel(header_frame, text="Study Heatmap (Last 35 Days)", font=("Helvetica", 18, "bold")).pack(side="left")
        
        total_mins = sum(self.mock_history)
        hours = total_mins // 60
        ctk.CTkLabel(header_frame, text=f"Total: {hours} hrs", font=("Helvetica", 14), text_color="#3498db").pack(side="right")

        # The Grid Area
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(padx=20, pady=10)

        # 7x5 Grid
        day_labels = ["M", "T", "W", "T", "F", "S", "S"]
        
        # 1. Draw Row Labels
        for row in range(7):
            ctk.CTkLabel(self.grid_frame, text=day_labels[row], font=("Helvetica", 10), text_color="gray").grid(row=row, column=0, padx=(0, 10), pady=2)

        # 2. Draw the Data Squares
        day_index = 0
        for col in range(1, 6): # 5 weeks (columns)
            for row in range(7): # 7 days (rows)
                if day_index < len(self.mock_history):
                    duration = self.mock_history[day_index]
                    square_color = self.get_color_for_duration(duration)
                    
                    
                    square = ctk.CTkFrame(self.grid_frame, width=20, height=20, fg_color=square_color, corner_radius=3)
                    square.grid(row=row, column=col, padx=2, pady=2)
                    
                    day_index += 1

        # Legend Area
        self.draw_legend()

    def draw_legend(self):
        legend_frame = ctk.CTkFrame(self, fg_color="transparent")
        legend_frame.pack(side="right", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(legend_frame, text="Less", font=("Helvetica", 10), text_color="gray").pack(side="left", padx=5)
        
        colors = ["#1e1e1e", "#0e4429", "#006d32", "#26a641", "#39d353"]
        for color in colors:
            ctk.CTkFrame(legend_frame, width=12, height=12, fg_color=color, corner_radius=2).pack(side="left", padx=2)
            
        ctk.CTkLabel(legend_frame, text="More", font=("Helvetica", 10), text_color="gray").pack(side="left", padx=5)


# ==========================================
# LOCAL TESTING BLOCK
# ==========================================
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("400x350")
    app.title("Module Test: Activity Heatmap")
    app.configure(fg_color="#1e1e1e")
    
    heatmap_module = ActivityHeatmap(app)
    heatmap_module.pack(fill="both", expand=True, padx=20, pady=20)
    
    app.mainloop()

