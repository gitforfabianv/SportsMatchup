from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from nba_api.teams_static import get_nba_teams
from nba_api.matchups import get_matchup_data
from nba_api.scrapers import scrape_team_wikipedia_data
from flask import jsonify, request
from nba_api.api import get_teams, fetch_team_details
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ASCII art for homepage
neo_art = """
⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀
⠀⠀⢀⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀
⠀⢠⣿⣿⣿⣿⣿⠿⠛⠛⠛⠛⠻⢿⣿⣿⣷⡀⠀⠀
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
⠀⢠⣿⣿⣿⣿⣿⠿⠛⠛⠛⠛⠻⢿⣿⣿⣷⡀⠀⠀
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
# HTML splash template
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
        <a href="/api/matchup/MIA/MIN">Mia vs Min</a> 
        <a href="/api/test-api">API PULL</a>
    </div>
</body>
<footer>
    <a href="/api/credits">CREDITS</a>
</footer>
</html>
"""

# Test page
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

# Route: Home splash page
@app.route('/')
def index():
    return render_template_string(template, neo_art=neo_art)

# Route: Test HTML page
@app.route('/api/test')
def test_page():
    return render_template_string(test_template, neo_art=agent_art)

# API: Test API call
@app.route('/api/test-api')
def test_api():
    teams_list = get_teams(use_scrape=False, use_pull=True)
    return jsonify({
        "message": f"API call successful. Found {len(teams_list)} teams using RapidAPI (pull).",
        "teams": teams_list
    })

# API: Get list of teams
@app.route('/api/teams')
def get_teams_list():
    use_scrape = request.args.get('scrape', 'false').lower() == 'true'
    use_pull = request.args.get('pull', 'false').lower() == 'true'
    teams_list = get_teams(use_scrape=use_scrape, use_pull=use_pull)

    if not teams_list:
        # If API returns nothing, use splash teams as fallback
        return jsonify(get_nba_teams())
    return jsonify(teams_list)

@app.route('/api/team/<string:shortname>', methods=['GET'])
def get_team_info(shortname):
    teams = get_nba_teams()
    team = next((t for t in teams if t['short_name'].lower() == shortname.lower()), None)

    if not team:
        return jsonify({"error": f"Team with short name '{shortname}' not found."}), 404

    data = scrape_team_wikipedia_data(team['name'])

    if not data:
        return jsonify({"error": "Could not scrape Wikipedia data for this team."}), 500

    return jsonify({
        "short_name": shortname.upper(),
        "franchise": team['name'],
        "wikipedia_data": data
    })
    
# API: Get team details
@app.route('/api/team-details/<string:team_id>')
def team_details(team_id):
    details = fetch_team_details(team_id)
    if details:
        return jsonify(details)
    return jsonify({"error": "No details found for the specified team ID."}), 404

# API: Team vs Team matchup
@app.route('/api/matchup/<string:team1>/<string:team2>')
def matchup(team1, team2):
    use_scrape = request.args.get('scrape', 'false').lower() == 'true'
    use_pull = request.args.get('pull', 'false').lower() == 'true'

    def teams_func():
        return get_teams(use_scrape=use_scrape, use_pull=use_pull)

    result, status = get_matchup_data(team1, team2, teams_func, fetch_team_details)

    return jsonify(result), status

# API: Credits
@app.route('/api/credits')
def credits():
    return jsonify({
        "credits": "Please consider sponsoring or buying me a coffee.",
        "github": "https://github.com/tedleyem", 
    })


if __name__ == '__main__':
    app.run(debug=True)
