import pandas as pd

def get_matchup_data(team1, team2, get_teams, fetch_team_details):
    """
    Returns matchup details between two teams or error info.

    Parameters:
    - team1, team2: full team names (e.g. "Miami Heat")
    - get_teams: function returning list of teams (from teams_static.py or API)
    - fetch_team_details: function that accepts a short_name and returns details

    Returns:
    - dict with matchup data or error
    - status code (200 or 404/500)
    """
    teams = get_teams()
    df = pd.DataFrame(teams)

    if 'name' not in df.columns or 'short_name' not in df.columns:
        return {"error": "Teams data missing required columns."}, 500

    team1_data = df[df['name'] == team1]
    team2_data = df[df['name'] == team2]

    if team1_data.empty or team2_data.empty:
        return {"error": "One or both of the specified teams do not exist."}, 404

    team1_short_name = team1_data.iloc[0]['short_name']
    team2_short_name = team2_data.iloc[0]['short_name']

    team1_details = fetch_team_details(team1_short_name)
    team2_details = fetch_team_details(team2_short_name)

    return {
        "team1": team1_details,
        "team2": team2_details,
    }, 200
