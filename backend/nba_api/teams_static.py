# Local TEAMS to scrape for the splash screen 

def get_nba_teams():
    """
    API Endpoint to return a list of NBA team IDs, names, and logos in JSON response.
    """
    teams = [
        {"short_name": "ATL", "name": "Atlanta Hawks", "image": "https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg"},
        {"short_name": "BOS", "name": "Boston Celtics", "image": "https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg"},
        {"short_name": "BKN", "name": "Brooklyn Nets", "image": "https://upload.wikimedia.org/wikipedia/en/4/40/Brooklyn_Nets_primary_icon_logo_2024.svg"},
        {"short_name": "CHA", "name": "Charlotte Hornets", "image": "https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg"},
        {"short_name": "CHI", "name": "Chicago Bulls", "image": "https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg"},
        {"short_name": "CLE", "name": "Cleveland Cavaliers", "image": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Cleveland_Cavaliers_logo.svg"},
        {"short_name": "DAL", "name": "Dallas Mavericks", "image": "https://upload.wikimedia.org/wikipedia/en/9/97/Dallas_Mavericks_logo.svg"},
        {"short_name": "DEN", "name": "Denver Nuggets", "image": "https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg"},
        {"short_name": "DET", "name": "Detroit Pistons", "image": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Logo_of_the_Detroit_Pistons.svg"},
        {"short_name": "GSW", "name": "Golden State Warriors", "image": "https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg"},
        {"short_name": "HOU", "name": "Houston Rockets", "image": "https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg"},
        {"short_name": "IND", "name": "Indiana Pacers", "image": "https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg"},
        {"short_name": "LAC", "name": "Los Angeles Clippers", "image": "https://upload.wikimedia.org/wikipedia/en/e/ed/Los_Angeles_Clippers_%282024%29.svg"},
        {"short_name": "LAL", "name": "Los Angeles Lakers", "image": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg"},
        {"short_name": "MEM", "name": "Memphis Grizzlies", "image": "https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg"},
        {"short_name": "MIA", "name": "Miami Heat", "image": "https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg"},
        {"short_name": "MIL", "name": "Milwaukee Bucks", "image": "https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg"},
        {"short_name": "MIN", "name": "Minnesota Timberwolves", "image": "https://upload.wikimedia.org/wikipedia/en/c/c2/Minnesota_Timberwolves_logo.svg"},
        {"short_name": "NOP", "name": "New Orleans Pelicans", "image": "https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg"},
        {"short_name": "NYK", "name": "New York Knicks", "image": "https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg"},
        {"short_name": "OKC", "name": "Oklahoma City Thunder", "image": "https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg"},
        {"short_name": "ORL", "name": "Orlando Magic", "image": "https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg"},
        {"short_name": "PHI", "name": "Philadelphia 76ers", "image": "https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg"},
        {"short_name": "PHX", "name": "Phoenix Suns", "image": "https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg"},
        {"short_name": "POR", "name": "Portland Trail Blazers", "image": "https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg"},
        {"short_name": "SAC", "name": "Sacramento Kings", "image": "https://upload.wikimedia.org/wikipedia/en/c/c7/SacramentoKings.svg"},
        {"short_name": "SAS", "name": "San Antonio Spurs", "image": "https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg"},
        {"short_name": "TOR", "name": "Toronto Raptors", "image": "https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg"},
        {"short_name": "UTA", "name": "Utah Jazz", "image": "https://upload.wikimedia.org/wikipedia/en/7/77/Utah_Jazz_logo_2025.svg"},
        {"short_name": "WAS", "name": "Washington Wizards", "image": "https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg"},
    ]
    return teams