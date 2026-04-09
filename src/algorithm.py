from datetime import datetime

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