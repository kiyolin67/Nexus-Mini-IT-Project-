from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

def calculate_time_decay(current_score, last_studied_date_str):
    """
    ### ALGORITHM: Spaced Repetition / Time Decay
    
    This function simulates human memory loss based on the Ebbinghaus Forgetting Curve.
    It calculates the days passed since a topic was last reviewed and applies a strict 
    5% penalty to the Mastery Score for every full week (7 days) of inactivity.

    """
    
    # Base Case: If the topic has never been studied, memory cannot decay.
    if not last_studied_date_str:
        return current_score, 0.0

    # Parse the string date from the database into a comparable Python Date object
    last_studied = datetime.strptime(last_studied_date_str, "%Y-%m-%d").date()
    today = datetime.now().date()

    # Calculate the absolute difference in days
    days_passed = (today - last_studied).days

    # Time Decay Logic: Only trigger if more than 7 days have passed
    if days_passed > 7:
        # Calculate how many full weeks have been missed (Floor division)
        weeks_missed = days_passed // 7
        
        # Calculate the total penalty (5% per week)
        penalty = weeks_missed * 5.0
        
        # Apply penalty, but use max() to enforce a hard floor so scores never drop below 0%
        new_score = max(current_score - penalty, 0.0)
        
        return round(new_score, 1), penalty

    # If studied within the last 7 days, memory retention is optimal. No penalty.
    return current_score, 0.0



###
# INSIGHT LOGIC
###

def get_ai_study_advice(topic_name, duration_mins, confidence_level):
    """
    ALGORITHM: AI-Generated Study Advice
    Takes the student's topic, study duration, and confidence level to generate personalized study advice using Google Gemini.
    """
    try:
        # 1. Load secret API key from .env file
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        # 2. Model 
        model = genai.GenerativeModel('gemini-1.5-flash')
        # 3. Construct Prompt with clear instructions and context
        prompt = f"""
        You are an expert study advisor for foundation university students. 
        A student has just studied '{topic_name}' for {duration_mins} minutes and rates their confidence level as {confidence_level}/5.

        Provide exactly 2-3 short sentences of actionable, scientific study advice based on this data.
        If they studied over 90 minutes, warn them about cognitive burnout.
        Do not use formatting like bolding or bullet points.
        """

        # 4. Call API and return clean and clear text
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        # Ensures if user has no Wifi, the app wont crash
        print(f"API Error: {e}")
        return "Insights offline. Remember to use Spaced Repetition and take a 15-minute break every hour to maximize retention!"



# ==========================================
# LOCAL TESTING BLOCK
# ==========================================
if __name__ == "__main__":
    from datetime import datetime, timedelta
    
    # Fake Dates for Testing
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    eight_days_ago = (today - timedelta(days=8)).strftime("%Y-%m-%d")
    three_months_ago = (today - timedelta(days=90)).strftime("%Y-%m-%d")
    
    # Test Case 1: Studied recently (Less than 7 days)
    print("\nTest 1: Studied Yesterday (Expect: No penalty)")
    score, penalty = calculate_time_decay(85.0, yesterday)
    print(f"Result -> New Score: {score} | Penalty Applied: {penalty}%")

    # Test Case 2: Just over a week (8 days)
    print("\nTest 2: Studied 8 days ago (Expect: 5% penalty)")
    score, penalty = calculate_time_decay(85.0, eight_days_ago)
    print(f"Result -> New Score: {score} | Penalty Applied: {penalty}%")

    # Test Case 3: Edge Case - Extreme Decay (Should hit the 0.0 floor, not go negative)
    print("\nTest 3: Studied 90 days ago with low score (Expect: Score hits 0.0, no negatives)")
    score, penalty = calculate_time_decay(30.0, three_months_ago)
    print(f"Result -> New Score: {score} | Penalty Applied: {penalty}%")

    # Test Case 4: Edge Case - Brand new topic
    print("\nTest 4: Never studied (Expect: 0 penalty)")
    score, penalty = calculate_time_decay(0.0, None)
    print(f"Result -> New Score: {score} | Penalty Applied: {penalty}%")

    # Test 5
    print("\nTest 5: Studied 15 days ago (Expect: 10% penalty)")
    

#===========================================