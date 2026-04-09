# 🧠 Nexus: Academic Analytics & Weakness Tracker

Nexus is a Python-based desktop study management system designed to help Foundation students at Multimedia University (MMU) track study sessions, evaluate their understanding, and identify weak foundational topics. 

Unlike standard to-do lists, Nexus utilizes a custom **Mastery Score Algorithm** and **Spaced Repetition (Time Decay)** to provide automated, scientifically-backed recommendations to prevent cognitive burnout and optimize study efficiency.



✨ Core Features
* **Algorithmic Mastery Tracking:** Calculates a normalized (0-100) comprehension score based on recent quiz scores, self-assessed confidence, and time invested.
* **Spaced Repetition Engine:** Automatically applies a "Time Decay" penalty to topics that haven't been reviewed in over 7 days to simulate human memory loss.
* **Scientific Insights:** Detects poor study habits (e.g., cramming for 2+ hours or high-friction burnout) and generates actionable, research-backed advice.
* **Prerequisite Mapping:** Hardcoded 1-to-1 dependency logic that automatically identifies if a student is failing an advanced topic because they lack the foundational prerequisites.
* **Dynamic Data Visualization:** Real-time Matplotlib integration displaying dynamic bar charts for instant visual feedback on academic standing.

---

🛠️ Tech Stack
* **Language:** Python 3
* **GUI Framework:** CustomTkinter (Minimalist Dark Mode UI)
* **Data Visualization:** Matplotlib
* **Database Management:** SQLite3 (Local file-based storage)

---

📂 Project Architecture


Nexus/
├── .gitignore
├── README.md
|
└── src/
    ├── main.py          
    ├── database.py      
    ├── algorithm.py     
    └── ui.py            
