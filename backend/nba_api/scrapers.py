import requests
from bs4 import BeautifulSoup

def scrape_team_wikipedia_data(team_name):
    """
    Scrapes Wikipedia for team details based on full name (e.g., 'Miami Heat').

    Returns a dict with team colors, location, arena, sponsor, founded etc.
    """
    try:
        search_url = f"https://en.wikipedia.org/wiki/{team_name.replace(' ', '_')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(search_url, headers=headers)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        infobox = soup.find("table", class_="infobox")

        data = {}
        rows = infobox.find_all("tr")

        for row in rows:
            header = row.find("th")
            value = row.find("td")
            if not header or not value:
                continue

            label = header.text.strip().lower()
            val_text = value.text.strip().replace("\xa0", " ")

            if "arena" in label:
                data["Arena"] = val_text
            elif "location" in label:
                data["Location"] = val_text
            elif "sponsor" in label:
                data["Main Sponsor"] = val_text
            elif "founded" in label:
                data["Founded"] = val_text
            elif "team colors" in label:
                data["Colors"] = val_text
            elif "colors" == label:
                data["Colors"] = val_text
            elif "president" in label:
                data["President"] = val_text

        return data if data else None

    except Exception as e:
        print(f"Error scraping Wikipedia: {e}")
        return None
