import json  # Import the json module for reading and writing JSON files

HIGH_SCORES_FILE = "high_scores.json"  # Define the file name for the high scores

# Function to load existing high scores from the high_scores file
def load_high_scores():
    try:
        with open(HIGH_SCORES_FILE, 'r') as file:
            high_scores_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is not a valid JSON, initialize an empty list
        high_scores_list = []

    return high_scores_list

# Function to save the updated high scores back to the high_scores file
def save_high_scores(high_scores_list):
    with open(HIGH_SCORES_FILE, 'w') as file:
        # Write the high scores list as a formatted JSON with an indentation of 2 spaces
        json.dump(high_scores_list, file, indent=2)

# Function to get the current highest score
def get_highest_score():
    high_score_list = load_high_scores()
    
    if high_score_list:
        highest_score = high_score_list[0]['score']
        return highest_score
    else:
        return 0 #there is not current high score
