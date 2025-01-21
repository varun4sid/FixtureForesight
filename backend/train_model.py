import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the dataset
data = pd.read_csv('fixture_dataset.csv')  # Update with the correct dataset path

# Define feature columns and target variables for training
feature_cols = [
    'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HomeTeamLP', 'AwayTeamLP',
    'HTFormPts', 'ATFormPts', 'HTWinStreak3', 'HTLossStreak3', 'ATWinStreak3', 
    'ATLossStreak3', 'HTGD', 'ATGD', 'DiffPts', 'DiffFormPts', 'DiffLP'
]
target_col_outcome = 'FTR'  # Target for match outcome prediction
target_col_home_goals = 'FTHG'  # Target for home goals prediction
target_col_away_goals = 'FTAG'  # Target for away goals prediction

# Create binary target for outcome (1 for Home win, 0 otherwise)
data['FTR_binary'] = data['FTR'].apply(lambda x: 1 if x == 'H' else 0)

# Split data into training (up to 2014-15 season) and test sets (2015-16 season)
data['Season'] = data['Date'].apply(lambda date: int(date[:4]) if int(date[5:7]) >= 7 else int(date[:4]) - 1)
train_data = data[data['Season'] < 2015]
test_data = data[data['Season'] == 2015]

# Define feature and target sets for each model
X_train = train_data[feature_cols]
y_train_outcome = train_data['FTR_binary']
y_train_home_goals = train_data[target_col_home_goals]
y_train_away_goals = train_data[target_col_away_goals]

# Train the models
outcome_model = RandomForestClassifier(random_state=0)
outcome_model.fit(X_train, y_train_outcome)
 
home_goal_model = RandomForestClassifier(random_state=0)
home_goal_model.fit(X_train, y_train_home_goals)

away_goal_model = RandomForestClassifier(random_state=0)
away_goal_model.fit(X_train, y_train_away_goals)

# Save all models into model.pkl
with open('model1.pkl', 'wb') as file:
    pickle.dump({
        'outcome_model': outcome_model,
        'home_goal_model': home_goal_model,
        'away_goal_model': away_goal_model
    }, file)

print("Models trained and saved to model.pkl")