import axios from "axios";

const API = axios.create({ baseURL: "http://127.0.0.1:5000/api" });

export const fetchTeams = () => API.get("/teams");
export const predictOutcome = (homeTeam, awayTeam) => API.post("/predict", {
    home_team: homeTeam,
    away_team: awayTeam
});
