import pandas as pd
import pickle

with open('model.pkl', 'rb') as file:
    models = pickle.load(file)

def predict_match_result(home_team, away_team, data):
    feature_cols = [
        'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HomeTeamLP', 'AwayTeamLP',
        'HTFormPts', 'ATFormPts', 'HTWinStreak3', 'HTLossStreak3', 'ATWinStreak3', 
        'ATLossStreak3', 'HTGD', 'ATGD', 'DiffPts', 'DiffFormPts', 'DiffLP'
    ]
    
    match_data = data[(data['HomeTeam'] == home_team) & (data['AwayTeam'] == away_team)]
    
    if match_data.empty:
        print(f"No match data available for {home_team} vs {away_team}.")
        return

    match_features = match_data[feature_cols]
    #outcome_model = models['outcome_model']
    home_goal_model = models['home_goal_model']
    away_goal_model = models['away_goal_model']
    
    #outcome_pred_binary = outcome_model.predict(match_features)
    predicted_home_goals = home_goal_model.predict(match_features)[0]
    predicted_away_goals = away_goal_model.predict(match_features)[0]
    
    if predicted_home_goals > predicted_away_goals:
        outcome_pred = 'H'
    elif predicted_home_goals < predicted_away_goals:
        outcome_pred = 'A'
    else:
        outcome_pred = 'D'
    
    print(f"Predicted Outcome: {outcome_pred}")
    print(f"Predicted Goals: {home_team} {predicted_home_goals} - {predicted_away_goals} {away_team}")

data = pd.read_csv('fixture_dataset.csv')

home_team = input("Enter Home Team: ")
away_team = input("Enter Away Team: ")

predict_match_result(home_team, away_team, data)