import os
import time
from dotenv import load_dotenv
from google import genai
import tkinter as tk
from tkinter import filedialog

def generate_quiz():
    """
    Takes pdf and generates quiz using google gemini
    """
    print("Nexus AI Loading Test Quiz Generation...")

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    file_path = filedialog.askopenfilename(
        title="Select PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        print("No file selected.")
        return

    print(f"Selected: {file_path}")

    # Load API key from .env file
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Reading and Uploading PDF
    # ADD A RETRY CUZ THE APP CAN CRASH OR THE API IS TOO OVERLOADED SO THIS MIGHT WORK IDK
    max_retries = 5

    for attempt in range(max_retries):
        try:
            print("Uploading PDF using Nexus AI...")
            uploaded_pdf = client.files.upload(file=file_path)
            
            print("Analyzing PDF with Nexus AI...")
            # REMEMBER TO CHANGE PROMPT IF ITS TOO NICHE
            prompt = """
            You are an expert university professor. A student has uploaded this document. Generate 5 multiple-choice questions that test the key concepts in this document. Each question should have 4 answer options, A through D, with only one correct answer. Format the output as follows: Question 1: [Question text]. Dont use bullet points or bolding. Just plain text. Include the answer key at the very bottom.
            """

            # Call API and return clean and clear text
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[uploaded_pdf, prompt]
            )

            print("\nNexus AI Quiz Generated:\n")
            print(response.text)
            
            return 

        except Exception as e:
            error_msg = str(e)

            # 503 - google sucks
            # 429 - too many requests from user probably cuz free tier
            # past 7pm is bad timing to use the API
            if "503" in error_msg or "UNAVAILABLE"  or "429" or "TOO MANY" in error_msg:
                wait_time = 2 ** attempt # power of 2 for exponential pattern
                print(f"Nexus AI is currently overloaded (Attempt {attempt + 1}/{max_retries}). Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"API Error: {e}")
                break # IF ITS NOT A 503 ERROR, THEN DONT RETRY BECAUSE IT WONT WORK

    # This will only print if the loop fails 3 times in a row
    print("Nexus AI Quiz Generation Test Failed.")

# INSIGHT LOGIC TEST
if __name__ == "__main__":
    generate_quiz()

# 2 SECONDS IS TOO SHORT
# maybe use geometric for the timer?