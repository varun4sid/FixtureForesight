from flask import Flask, request, jsonify
import pandas as pd
import pickle
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Load your pre-trained models
with open('model.pkl', 'rb') as model_file:
    models = pickle.load(model_file)

# Load the dataset (replace 'your_dataset.csv' with your actual dataset filename)
data = pd.read_csv('fixture_dataset.csv')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    home_team = request.json.get('home_team')
    away_team = request.json.get('away_team')

    # Validate input
    if not home_team or not away_team:
        return jsonify({'error': 'Please provide both home and away team names.'}), 400

    # Predict the match result
    feature_cols = [
        'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HomeTeamLP', 'AwayTeamLP',
        'HTFormPts', 'ATFormPts', 'HTWinStreak3', 'HTLossStreak3', 'ATWinStreak3', 
        'ATLossStreak3', 'HTGD', 'ATGD', 'DiffPts', 'DiffFormPts', 'DiffLP'
    ]

    # Filter data for the specific match
    match_data = data[(data['HomeTeam'] == home_team) & (data['AwayTeam'] == away_team)]

    if match_data.empty:
        return jsonify({'error': f'No match data available for {home_team} vs {away_team}.'}), 404

    # Use only the relevant feature columns
    match_features = match_data[feature_cols]

    # Load individual models for outcome prediction and goal prediction
    outcome_model = models['outcome_model']
    home_goal_model = models['home_goal_model']
    away_goal_model = models['away_goal_model']

    # Predict outcome
    outcome_pred_binary = outcome_model.predict(match_features)

    # Predict goals scored by each team
    predicted_home_goals = int(home_goal_model.predict(match_features)[0])
    predicted_away_goals = int(away_goal_model.predict(match_features)[0])

    # Determine the outcome based on predicted scores
    if predicted_home_goals > predicted_away_goals:
        outcome_pred = 'H'  # Home win
    elif predicted_home_goals < predicted_away_goals:
        outcome_pred = 'A'  # Away win
    else:
        outcome_pred = 'D'  # Draw

    # Prepare response
    response = {
        'predicted_outcome': outcome_pred,
        'predicted_goals': {
            'home_team': predicted_home_goals,
            'away_team': predicted_away_goals
        }
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
