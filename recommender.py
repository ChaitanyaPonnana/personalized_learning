import pandas as pd

# Load content dataset
content = pd.read_csv("data/content.csv")

def recommend(interests, score):
    # Decide difficulty based on score
    if score < 50:
        difficulty = "Easy"
    elif score <= 75:
        difficulty = "Medium"
    else:
        difficulty = "Hard"
    
    # Filter content based on interests + difficulty
    results = content[
        (content["subject"].isin(interests)) &
        (content["difficulty"] == difficulty)
    ]
    return results
