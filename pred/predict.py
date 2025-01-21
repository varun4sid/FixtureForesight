import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load historical dataset and fixtures
historical_data = pd.read_csv('historical_data.csv')
fixtures_2017_18 = pd.read_csv('dataset.csv')

# Encode result column: H = 1 (home win), A = -1 (away win), D = 0 (draw)
historical_data['result_encoded'] = historical_data['result'].map({'H': 1, 'A': -1, 'D': 0})

# Feature Engineering: Calculate average goals scored and conceded for each team over past seasons
team_stats = historical_data.groupby('home_team').agg(
    avg_goals_scored=('home_goals', 'mean'),
    avg_goals_conceded=('away_goals', 'mean')
).reset_index()

# Merge team strength features into historical data
historical_data = historical_data.merge(team_stats, left_on='home_team', right_on='home_team', how='left')
historical_data = historical_data.merge(team_stats, left_on='away_team', right_on='home_team', suffixes=('_home', '_away'))

# Select features and target variable
X = historical_data[['avg_goals_scored_home', 'avg_goals_conceded_home', 'avg_goals_scored_away', 'avg_goals_conceded_away']]
y = historical_data['result_encoded']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.2f}')

# Prepare 2017-18 fixtures for prediction
# Merge team strength into the fixtures dataset for 2017-18
fixtures_2017_18 = fixtures_2017_18.merge(team_stats, left_on='home_team', right_on='home_team', how='left')
fixtures_2017_18 = fixtures_2017_18.merge(team_stats, left_on='away_team', right_on='home_team', suffixes=('_home', '_away'))

# Prepare features for prediction
X_fixtures = fixtures_2017_18[['avg_goals_scored_home', 'avg_goals_conceded_home', 'avg_goals_scored_away', 'avg_goals_conceded_away']]
fixtures_2017_18['predicted_result'] = model.predict(X_fixtures)

# Generate the 2017-18 Season Table
# Extract unique teams from the 2017-18 fixtures to initialize the table
unique_teams = pd.concat([fixtures_2017_18['home_team'], fixtures_2017_18['away_team']]).drop_duplicates().values
table = pd.DataFrame(unique_teams, columns=['team'])
table.set_index('team', inplace=True)
table[['points', 'games_played', 'goals_scored', 'goals_conceded', 'goal_difference']] = 0

# Update table based on predicted results
for _, row in fixtures_2017_18.iterrows():
    home_team = row['home_team']
    away_team = row['away_team']
    predicted_result = row['predicted_result']
    
    # Update points and games played based on prediction
    table.loc[home_team, 'games_played'] += 1
    table.loc[away_team, 'games_played'] += 1
    
    if predicted_result == 1:  # Home win
        table.loc[home_team, 'points'] += 3
    elif predicted_result == -1:  # Away win
        table.loc[away_team, 'points'] += 3
    else:  # Draw
        table.loc[home_team, 'points'] += 1
        table.loc[away_team, 'points'] += 1
    
# Calculate goal difference
table['goal_difference'] = table['goals_scored'] - table['goals_conceded']

# Sort the table by points and goal difference to reflect standings
table = table.sort_values(by=['points', 'goal_difference'], ascending=[False, False])

# Display the table
print(table)
