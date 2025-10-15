import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

# Suppress the InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

API_KEY = "2a4ff8e817msh29f1a76b1f56ec9p13eb64jsn5a2da6223d74"
API_HOST = "nba-api-free-data.p.rapidapi.com"

def scrape_teams():
    print("Scraping teams from Basketball Reference...")
    url = 'https://www.basketball-reference.com/teams/'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'teams_active'})

    teams = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 13:  # Ensure we have sufficient cells
            anchor_tag = cells[0].find('a')
            short_name = anchor_tag['href'].split('/')[-2] if anchor_tag else 'N/A'
            
            team = {
                'franchise': cells[0].text.strip(),  # Franchise
                'AGE': cells[4].text.strip(),  # Years of existence (AGE)
                'conference': cells[11].text.strip(),  # Conference
                'championships_won': int(cells[12].text.strip()) if cells[12].text.strip().isdigit() else 0,  # Championships won
                'short_name': short_name    # Adding this to use for fetching details
            }
            teams.append(team)

    # Sort teams by championships in descending order
    teams.sort(key=lambda x: x['championships_won'], reverse=True)
    print(f"Scraped data: {teams}")
    return teams

def fetch_team_details(short_name):
    print(f"Fetching details for team: {short_name}")
    url = f'https://www.basketball-reference.com/teams/{short_name}/'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', {'class': 'content'})
    
    if not content:
        return {}
    
    details = {
        'location': content.find('div', string='Location:').find_next_sibling().text.strip(),
        'team_name': content.find('div', string='Team Names:').find_next_sibling().text.strip(),
        'seasons': content.find('div', string='Seasons:').find_next_sibling().text.strip(),
        'record': content.find('div', string='Record:').find_next_sibling().text.strip(),
        'playoff_appearances': content.find('div', string='Playoff Appearances:').find_next_sibling().text.strip(),
        'championships': content.find('div', string='Championships:').find_next_sibling().text.strip(),
    }
    
    return details

def fetch_division_teams(endpoint):
    url = f"https://{API_HOST}{endpoint}"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    response = requests.get(url, headers=headers, verify=False)
    
    if response.ok:
        print(f"Response from {endpoint}: {response.json()}")
        try:
            return response.json()['response']['teamList']
        except KeyError:
            print(f"Key 'teamList' not found in the response for {endpoint}")
            return []
    else:
        print(f"Error fetching data from {endpoint}: {response.status_code}")
        return []

def get_team_logo(team_id):
    url = f"https://{API_HOST}/nba-team-logo"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    params = {"teamid": team_id}
    response = requests.get(url, headers=headers, params=params, verify=False)
    if response.status_code == 200:
        return response.json().get('logo', '')
    return ''

def get_team_details(team_id):
    url = f"https://{API_HOST}/nba-team-detail"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    params = {"teamid": team_id}
    response = requests.get(url, headers=headers, params=params, verify=False)
    if response.status_code == 200:
        return response.json()
    return {}

def get_team_records(team_id):
    url = f"https://{API_HOST}/nba-team-record"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    params = {"teamid": team_id}
    response = requests.get(url, headers=headers, params=params, verify=False)
    if response.status_code == 200:
        return response.json()
    return {}

def get_teams(use_scrape=False, use_pull=False):
    print(f"Fetching teams. Use scrape: {use_scrape}, Use pull: {use_pull}")

    if use_pull:
        print("Using RapidAPI to fetch teams...")
        divisions = {
            "Southwest": "/nba-southwest-team-list",
            "Pacific": "/nba-pacific-team-list",
            "Northwest": "/nba-northwest-team-list",
            "Southeast": "/nba-southeast-team-list",
            "Central": "/nba-central-team-list",
            "Atlantic": "/nba-atlantic-team-list"
        }
        all_teams = []
        for division_name, endpoint in divisions.items():
            teams = fetch_division_teams(endpoint)
            for team in teams:
                team_id = team.get('id', None)  # Only fetch if there is an id
                if team_id:
                    team_details = get_team_details(team_id)
                    team['division'] = division_name
                    team['location'] = team_details.get('location', 'N/A')
                all_teams.append(team)
        return all_teams

    # Otherwise, default to scraping
    return scrape_teams()