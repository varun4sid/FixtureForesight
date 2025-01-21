import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm = () => {
    const [homeTeam, setHomeTeam] = useState('');
    const [awayTeam, setAwayTeam] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState('');

    const handlePredict = async (e) => {
        e.preventDefault(); // Prevent form submission

        if (!homeTeam || !awayTeam) {
            setError('Please enter both team names.');
            return;
        }

        try {
            const response = await axios.post('http://127.0.0.1:5000/predict', {
                home_team: homeTeam,
                away_team: awayTeam,
            });
            setPrediction(response.data);
            setError(''); // Clear any previous errors
        } catch (err) {
            if (err.response && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError('An unexpected error occurred. Please try again.');
            }
            setPrediction(null); // Clear previous predictions on error
        }
    };

    return (
        <div style={{ textAlign: 'center', margin: '20px' }}>
            <h2>Predict Match Outcome</h2>
            <form onSubmit={handlePredict}>
                <input
                    type="text"
                    placeholder="Enter Home Team"
                    value={homeTeam}
                    onChange={(e) => setHomeTeam(e.target.value)}
                    style={{ margin: '5px', padding: '10px', width: '200px' }}
                />
                <input
                    type="text"
                    placeholder="Enter Away Team"
                    value={awayTeam}
                    onChange={(e) => setAwayTeam(e.target.value)}
                    style={{ margin: '5px', padding: '10px', width: '200px' }}
                />
                <button type="submit" style={{ margin: '5px', padding: '10px' }}>
                    Predict
                </button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {prediction && (
                <div>
                    <h3>Prediction Result:</h3>
                    <p>Predicted Outcome: {prediction.predicted_outcome}</p>
                    <p>
                        Predicted Goals: {prediction.predicted_goals.home_team} -{' '}
                        {prediction.predicted_goals.away_team}
                    </p>
                </div>
            )}
        </div>
    );
};

export default PredictionForm;
