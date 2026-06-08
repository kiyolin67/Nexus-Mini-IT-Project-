import customtkinter as ctk

class FocusTimerWindow(ctk.CTkToplevel):
    def __init__(self, parent, subject_name, on_save_callback):
        super().__init__(parent)
        
        self.title("Active Focus Session")
        self.geometry("450x500")
        self.configure(fg_color="#1e1e1e")
        self.attributes('-topmost', True)

        self.protocol("WM_DELETE_WINDOW", self.stop_timer)  # Ensure timer stops if window is closed
        
        self.on_save_callback = on_save_callback
        self.subject_name = subject_name
        
        self.running = False
        self.time_elapsed = 0 
        self.final_minutes = 0

        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, text="Focus Session", font=("Helvetica", 28, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(self, text=f"Studying: {self.subject_name}", font=("Helvetica", 16), text_color="#3498db").pack(pady=(0, 20))

        self.clock_label = ctk.CTkLabel(self, text="00:00", font=("Helvetica", 80, "bold"))
        self.clock_label.pack(pady=20)

        self.controls = ctk.CTkFrame(self, fg_color="transparent")
        self.controls.pack(pady=10)

        self.btn_start = ctk.CTkButton(self.controls, text="Start", fg_color="#2ecc71", hover_color="#27ae60", command=self.start_timer, width=100)
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = ctk.CTkButton(self.controls, text="Stop & Log", fg_color="#e74c3c", hover_color="#c0392b", command=self.stop_timer, width=100, state="disabled")
        self.btn_stop.pack(side="left", padx=10)

        # Hidden Logging Area
        self.logging_area = ctk.CTkFrame(self, fg_color="transparent")
        
        ctk.CTkLabel(self.logging_area, text="Session Complete! Rate your confidence:", font=("Helvetica", 14, "bold")).pack(pady=(20, 5))
        self.slider_conf = ctk.CTkSlider(self.logging_area, from_=1, to=5, number_of_steps=4)
        self.slider_conf.pack(pady=10)
        
        self.btn_save = ctk.CTkButton(self.logging_area, text="Save to Database", fg_color="#f39c12", hover_color="#d35400", command=self.save_to_db)
        self.btn_save.pack(pady=10)

    def update_clock(self):
        if self.running:
            self.time_elapsed += 1
            minutes = self.time_elapsed // 60
            seconds = self.time_elapsed % 60
            self.clock_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.after(1000, self.update_clock)

    def start_timer(self):
        self.running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.update_clock()

    def stop_timer(self):
        self.running = False
        self.btn_stop.configure(state="disabled")
        self.final_minutes = max(1, self.time_elapsed // 60) 
        self.logging_area.pack(pady=20, fill="x", padx=40)

    def save_to_db(self):
        confidence = int(self.slider_conf.get())
        
        # Trigger the bridge function back in main.py
        self.on_save_callback(self.subject_name, self.final_minutes, confidence)
        
        # Close the popup window
        self.destroy()