from flask import Flask, jsonify, render_template_string, request
import json
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS # CORS (Cross-Origin Resource Sharing) issue.

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for dev

# ASCII art of Neo
neo_art = """
⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀
⠀⠀⢀⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀
⠀⢠⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣷⡀⠀
⠀⢸⣿⡿⠋⠁⠀⠀⠀⠉⠉⠀⠀⠀⠀⠈⢹⣿⡇⠀
⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀
⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀
⠀⢸⣿⣠⣴⣶⣶⣶⣦⣀⣀⣴⣶⣶⣶⣤⣄⣿⡇⡀
⣿⣿⣿⠻⣿⣿⣿⣿⣿⠟⠻⣿⣿⣿⣿⣿⠟⣿⣿⣿
⣿⣿⣿⠀⠈⠉⠛⠋⠉⠀⠀⠉⠙⠛⠉⠁⠀⣿⣿⣿
⠙⢿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⠃
⠀⠸⣿⣧⠀⠀⠀⢀⣀⣀⣀⣀⡀⠀⠀⠀⣼⣿⠇⠀
⠀⠀⠙⢿⣷⣄⠀⠈⠉⠉⠉⠉⠁⠀⣠⣾⡿⠃⠀⠀
⠀⠀⠀⢸⣿⣿⣷⣤⣀⣀⣀⣀⣤⣾⣿⣿⡅⠀⠀⠀
⠀⠀⢰⣿⣿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⡄⠀⠀
⠀⠀⠻⠿⠿⠿⠿⠿⠿⠷⠴⠿⠿⠿⠿⠿⠿⠇⠀⠀
"""
# ASCII art of Agent Smith
agent_art = """
⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀
⠀⠀⢀⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀
⠀⢠⣿⣿⣿⣿⣿⠿⠛⠛⠛⠛⠻⢿⣿⣿⣷⡀⠀
⠀⢸⣿⡿⠋⠁⠀⠀⠀ⴾⵉⴾ⠀⠀⠀⠈⢹⣿⡇⠀
⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀|⠀⠀⠀⠀⠀⠀⣿⡇⠀
⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀|⠀⠀⠀⠀⠀⠀⣿⡇⠀
⠀⢸⣿⣠⣴⣶⣶⣶⣦⣀⣀⣴⣶⣶⣶⣤⣄⣿⡇⡀
⣿⣿⣿⠻⣿⣿⣿⣿⣿⠟⠻⣿⣿⣿⣿⣿⠟⣿⣿⣿
⣿⣿⣿⠀⠈⠉⠛⠋⠉⠀⠀⠉⠙⠛⠉⠁⠀⣿⣿⣿
⠙⢿⣿⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⣿⡿⠃
⠀⠸⣿⣧⠀⠀⠀⠛⠿⠿⠿⠿⠿⠛⠀⠀⣼⣿⠇⠀
⠀⠀⠙⢿⣷⣄⠀⠰⣿⣿⣿⣿⠆⠀⣠⣾⡿⠃⠀⠀
⠀⠀⠀⢸⣿⣿⣷⣤⣀⣀⣀⣀⣤⣾⣿⣿⡅⠀⠀⠀
⠀⠀⢰⣿⣿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⡄⠀⠀
⠀⠀⠻⠿⠿⠿⠿⠿⠿⠷⠴⠿⠿⠿⠿⠿⠿⠇⠀⠀
"""

# Basic HTML template for the main page
template = """
<!DOCTYPE html>
<html>
<head>
    <title>What if I told you</title>
    <style>
        body {
            background-color: black;
            color: #00FF00;
            font-family: 'Courier New', monospace;
            text-align: center;
            margin-top: 50px;
        }
        pre {
            display: inline-block;
            text-align: left;
        }
        .links {
            margin-top: 20px;
        }
        .links a {
            color: #00FF00;
            margin: 0 15px;
            text-decoration: none;
            font-size: 18px;
        }
        .links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <pre>{{ neo_art }}</pre>
    <p>Just take the blue pill</p>
    <div class="links">
        <a href="/api/test">TEST</a>
        <a href="/api/teams">TEAMS</a>
        <a href="/api/test">TEST</a>
        <a href="/api/matchups?team1=MIA&team2=MIN">Mia vs Min</a>
    </div>
</body>
</html>
"""

#Test template 
test_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Test</title>
    <style>
        body {
            background-color: black;
            color: #00FF00;
            font-family: 'Courier New', monospace;
            text-align: center;
            margin-top: 50px;
        }
        pre {
            display: inline-block;
            text-align: left;
        }
        .links {
            margin-top: 20px;
        }
        .links a {
            color: #00FF00;
            margin: 0 15px;
            text-decoration: none;
            font-size: 18px;
        }
        .links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <pre>{{ neo_art }}</pre>
    <p>This is a test, this is only a test.</p>
    <div class="links"> 
        <a href="/">HOME</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(template, neo_art=neo_art)

@app.route('/api/test')
def get_test():
    return render_template_string(test_template, neo_art=agent_art)

@app.route("/api/teams", methods=["GET"])
def get_nba_teams():
    """
    API Endpoint to return a list of NBA team IDs, names, and logos in JSON response.
    """
    teams = [
        {"id": "ATL", "name": "Atlanta Hawks", "image": "https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg"},
        {"id": "BOS", "name": "Boston Celtics", "image": "https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg"},
        {"id": "BKN", "name": "Brooklyn Nets", "image": "https://upload.wikimedia.org/wikipedia/en/4/40/Brooklyn_Nets_primary_icon_logo_2024.svg"},
        {"id": "CHA", "name": "Charlotte Hornets", "image": "https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg"},
        {"id": "CHI", "name": "Chicago Bulls", "image": "https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg"},
        {"id": "CLE", "name": "Cleveland Cavaliers", "image": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Cleveland_Cavaliers_logo.svg"},
        {"id": "DAL", "name": "Dallas Mavericks", "image": "https://upload.wikimedia.org/wikipedia/en/9/97/Dallas_Mavericks_logo.svg"},
        {"id": "DEN", "name": "Denver Nuggets", "image": "https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg"},
        {"id": "DET", "name": "Detroit Pistons", "image": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Logo_of_the_Detroit_Pistons.svg"},
        {"id": "GSW", "name": "Golden State Warriors", "image": "https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg"},
        {"id": "HOU", "name": "Houston Rockets", "image": "https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg"},
        {"id": "IND", "name": "Indiana Pacers", "image": "https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg"},
        {"id": "LAC", "name": "Los Angeles Clippers", "image": "https://upload.wikimedia.org/wikipedia/en/e/ed/Los_Angeles_Clippers_%282024%29.svg"},
        {"id": "LAL", "name": "Los Angeles Lakers", "image": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg"},
        {"id": "MEM", "name": "Memphis Grizzlies", "image": "https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg"},
        {"id": "MIA", "name": "Miami Heat", "image": "https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg"},
        {"id": "MIL", "name": "Milwaukee Bucks", "image": "https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg"},
        {"id": "MIN", "name": "Minnesota Timberwolves", "image": "https://upload.wikimedia.org/wikipedia/en/c/c2/Minnesota_Timberwolves_logo.svg"},
        {"id": "NOP", "name": "New Orleans Pelicans", "image": "https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg"},
        {"id": "NYK", "name": "New York Knicks", "image": "https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg"},
        {"id": "OKC", "name": "Oklahoma City Thunder", "image": "https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg"},
        {"id": "ORL", "name": "Orlando Magic", "image": "https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg"},
        {"id": "PHI", "name": "Philadelphia 76ers", "image": "https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg"},
        {"id": "PHX", "name": "Phoenix Suns", "image": "https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg"},
        {"id": "POR", "name": "Portland Trail Blazers", "image": "https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg"},
        {"id": "SAC", "name": "Sacramento Kings", "image": "https://upload.wikimedia.org/wikipedia/en/c/c7/SacramentoKings.svg"},
        {"id": "SAS", "name": "San Antonio Spurs", "image": "https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg"},
        {"id": "TOR", "name": "Toronto Raptors", "image": "https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg"},
        {"id": "UTA", "name": "Utah Jazz", "image": "https://upload.wikimedia.org/wikipedia/en/7/77/Utah_Jazz_logo_2025.svg"},
        {"id": "WAS", "name": "Washington Wizards", "image": "https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg"},
    ]
    return jsonify(teams)

@app.route("/api/matchups", methods=["GET"])
def get_matchups():
    """
    API Endpoint to retrieve all-time head-to-head matchup data between two NBA teams.
    Expects 'team1' and 'team2' as query parameters (e.g., /api/matchups?team1=Miami%20Heat&team2=Minnesota%20Timberwolves).
    """
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    if not team1 or not team2:
        return jsonify({"error": "Both team1 and team2 query parameters are required"}), 400

    # Map team names to URL-friendly format
    team_map = {
        "Atlanta Hawks": "hawks",
        "Boston Celtics": "celtics",
        "Brooklyn Nets": "nets",
        "Charlotte Hornets": "hornets",
        "Chicago Bulls": "bulls",
        "Cleveland Cavaliers": "cavaliers",
        "Dallas Mavericks": "mavericks",
        "Denver Nuggets": "nuggets",
        "Detroit Pistons": "pistons",
        "Golden State Warriors": "warriors",
        "Houston Rockets": "rockets",
        "Indiana Pacers": "pacers",
        "Los Angeles Clippers": "clippers",
        "Los Angeles Lakers": "lakers",
        "Memphis Grizzlies": "grizzlies",
        "Miami Heat": "heat",
        "Milwaukee Bucks": "bucks",
        "Minnesota Timberwolves": "timberwolves",
        "New Orleans Pelicans": "pelicans",
        "New York Knicks": "knicks",
        "Oklahoma City Thunder": "thunder",
        "Orlando Magic": "magic",
        "Philadelphia 76ers": "76ers",
        "Phoenix Suns": "suns",
        "Portland Trail Blazers": "trail_blazers",
        "Sacramento Kings": "kings",
        "San Antonio Spurs": "spurs",
        "Toronto Raptors": "raptors",
        "Utah Jazz": "jazz",
        "Washington Wizards": "wizards"
    }

    if team1 not in team_map or team2 not in team_map:
        return jsonify({"error": "Invalid team name(s). Please use team names from /api/teams."}), 400

    # Construct the URL (e.g., https://www.landofbasketball.com/head_to_head/heat_vs_timberwolves_all_time.htm)
    team1_slug = team_map[team1]
    team2_slug = team_map[team2]
    url = f"https://www.landofbasketball.com/head_to_head/{team1_slug}_vs_{team2_slug}_all_time.htm"

    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the all-time head-to-head record
        # The record is typically in a section like "All-Time Head To Head"
        record_section = soup.find('div', class_='cont-wide')
        if not record_section:
            return jsonify({"error": "Could not find head-to-head data on the page"}), 404

        # Extract total games played
        total_games_text = record_section.find('h2', string=lambda text: 'Total Games Played' in text if text else False)
        if not total_games_text:
            return jsonify({"error": "Could not find total games played data"}), 404

        total_games = total_games_text.text.strip().split('(')[0].replace('Total Games Played', '').strip()

        # Find the regular season summary
        regular_season_section = soup.find('h2', string=lambda text: 'NBA Regular Season' in text if text else False)
        if not regular_season_section:
            return jsonify({"error": "Could not find regular season data"}), 404

        # Extract wins and losses
        wins_text = regular_season_section.find_next('p', string=lambda text: 'All-Time Record' in text if text else False)
        if not wins_text:
            return jsonify({"error": "Could not find wins/losses data"}), 404

        wins_lines = wins_text.text.strip().split('\n')
        team1_wins = next((line for line in wins_lines if team1 in line), None)
        team2_wins = next((line for line in wins_lines if team2 in line), None)

        if not team1_wins or not team2_wins:
            return jsonify({"error": "Could not parse wins/losses data"}), 404

        team1_wins_count = team1_wins.split()[2]  # e.g., "Miami Heat 36 Wins" -> "36"
        team2_wins_count = team2_wins.split()[2]  # e.g., "Minnesota Timberwolves 34 Wins" -> "34"

        # Construct response
        result = {
            "team1": team1,
            "team2": team2,
            "total_games_played": total_games,
            "regular_season": {
                f"{team1}_wins": team1_wins_count,
                f"{team2}_wins": team2_wins_count
            },
            "source_url": url
        }

        return jsonify(result)

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error processing data: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
