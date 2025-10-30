# team_totals_all_teams.py
import json
import logging
import random
import time
from pathlib import Path
from typing import Optional, List, Dict
from collections import OrderedDict
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------- CONFIG ----------------
SEASON = 2025
OUTPUT_FILE = Path("team_totals_all_teams.json")
HEADLESS = True
PROXIES: List[str] = []  # optional proxy list
PAGE_LOAD_WAIT = 12
ELEMENT_WAIT = 10
SAVE_EVERY = 1
# ----------------------------------------

TEAM_MAP = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHO", "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "LA Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP", "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR", "Utah Jazz": "UTA", "Washington Wizards": "WAS"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36",
]

# ---------------- HELPERS ----------------

def create_stealth_driver(proxy: Optional[str] = None, headless: bool = True):
    options = uc.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    ua = random.choice(USER_AGENTS)
    options.add_argument(f"--user-agent={ua}")
    if proxy:
        options.add_argument(f"--proxy-server=http://{proxy}")
    driver = uc.Chrome(options=options, use_subprocess=True)
    try:
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            """
        })
    except Exception:
        pass
    return driver

def safe_quit(driver):
    if driver:
        try:
            driver.quit()
        except Exception:
            pass

def extract_boxscore_links_from_driver(driver) -> List[str]:
    anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='/boxscores/']")
    links = []
    for a in anchors:
        href = a.get_attribute("href")
        if href and href.endswith(".html") and "/boxscores/" in href:
            links.append(href)
    return list(dict.fromkeys(links))  # dedupe

def parse_team_totals_from_html(html: str) -> Optional[Dict[str, Dict[str, str]]]:
    """
    Robust parsing of Team Totals table(s) with correct header alignment.
    Returns an OrderedDict per team so the JSON preserves the table order.
    """
    soup = BeautifulSoup(html, "html.parser")
    totals_per_team: Dict[str, Dict[str, str]] = {}

    for table in soup.find_all("table"):
        table_id = table.get("id", "")
        # skip irrelevant tables
        if not table_id.startswith("box-") or "-game-" not in table_id:
            continue

        # team code often like "box-ATL-game-basic"
        team_code = table_id.split("-")[1].upper() if "-" in table_id else table_id.upper()

        # find the most-likely header row: the last <tr> inside <thead>
        headers: List[str] = []
        thead = table.find("thead")
        if thead:
            header_rows = thead.find_all("tr")
            if header_rows:
                header_row = header_rows[-1]  # usually the stat names row
                for th in header_row.find_all(["th", "td"]):
                    # prefer data-stat attribute, else normalized text
                    data_stat = th.get("data-stat")
                    if data_stat and data_stat.strip():
                        headers.append(data_stat.strip())
                    else:
                        txt = th.get_text(strip=True)
                        headers.append(txt.lower().replace(" ", "_") if txt else "")
        else:
            # no thead: attempt to find first header row inside tbody (rare)
            first_row = table.find("tr")
            if first_row:
                for th in first_row.find_all(["th","td"]):
                    data_stat = th.get("data-stat")
                    if data_stat and data_stat.strip():
                        headers.append(data_stat.strip())
                    else:
                        txt = th.get_text(strip=True)
                        headers.append(txt.lower().replace(" ", "_") if txt else "")

        # if headers empty -> skip table
        if not headers:
            logging.debug(f"Skipping table {table_id} because headers could not be determined.")
            continue

        # detect leading player/starters column and set offset
        header_offset = 0
        if headers:
            lead = headers[0].lower() if isinstance(headers[0], str) else ""
            # common possible leading header names: 'player', 'starters', 'player_name', ''
            if "player" in lead or "starter" in lead or lead == "" or lead.startswith("starters"):
                header_offset = 1

        # Now find the Team Totals row(s)
        for tr in table.find_all("tr"):
            th_player = tr.find("th", {"data-stat": "player"})
            if not th_player:
                # some tables may not use data-stat attr for the leading TH -- also try text
                # fallback: check first th text
                first_th = tr.find("th")
                if not first_th:
                    continue
                if first_th.get_text(strip=True) not in ("Team Totals", "Team Totals*"):
                    continue
            else:
                # ensure it matches "Team Totals"
                if th_player.get_text(strip=True) != "Team Totals":
                    continue

            # At this point, we have the Team Totals row for this table
            tds = tr.find_all("td")
            # Create ordered mapping to preserve order
            team_stats = OrderedDict()

            for idx, td in enumerate(tds):
                header_idx = idx + header_offset
                if header_idx < len(headers):
                    stat_name = headers[header_idx]
                    if stat_name == "":
                        # fallback to positional name
                        stat_name = f"col_{idx}"
                else:
                    # fallback when header shorter than td list
                    stat_name = f"col_{idx}"
                stat_value = td.get_text(strip=True)
                team_stats[stat_name] = stat_value

            # merge stats across tables (basic/advanced). Keep insertion order: earlier tables first.
            if team_code not in totals_per_team:
                totals_per_team[team_code] = OrderedDict()
            # Overwrite or add keys from this table
            totals_per_team[team_code].update(team_stats)

    # Convert OrderedDict back to normal dicts (but they preserve insertion order in Python 3.7+)
    if totals_per_team:
        return {k: dict(v) for k, v in totals_per_team.items()}
    return None


# ---------------- TEAM SCRAPER ----------------

def scrape_team(team_code: str, headless: bool = HEADLESS, proxies: Optional[List[str]] = None):
    proxies = proxies or []
    results = []
    progress_file = OUTPUT_FILE.with_suffix(f".{team_code}.progress.json")
    schedule_url = f"https://www.basketball-reference.com/teams/{team_code}/{SEASON}_games.html"

    if progress_file.exists():
        try:
            results = json.loads(progress_file.read_text(encoding="utf-8"))
            logging.info(f"[{team_code}] Loaded {len(results)} games from progress file.")
        except Exception:
            results = []

    # ------------------- create fresh driver -------------------
    driver = None
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            driver = create_stealth_driver(headless=headless)
            logging.info(f"[{team_code}] Opening schedule page (attempt {attempt})...")
            driver.get(schedule_url)
            WebDriverWait(driver, PAGE_LOAD_WAIT).until(
                EC.presence_of_element_located((By.ID, "games"))
            )
            break
        except Exception as e:
            logging.warning(f"[{team_code}] Failed to load schedule page: {e}")
            safe_quit(driver)
            driver = None
            time.sleep(3)
    else:
        logging.error(f"[{team_code}] Could not load schedule page. Skipping team.")
        return results

    # ------------------- scrape boxscores -------------------
    try:
        links = extract_boxscore_links_from_driver(driver)
        logging.info(f"[{team_code}] Found {len(links)} boxscore links.")

        for idx, url in enumerate(links, start=1):
            try:
                driver.get(url)
                WebDriverWait(driver, ELEMENT_WAIT).until(
                    EC.presence_of_element_located((By.XPATH, "//th[@data-stat='player' and text()='Team Totals']"))
                )
                html = driver.page_source
                totals = parse_team_totals_from_html(html)

                if totals and team_code in totals:
                    game_record = {
                        "team": team_code,
                        "game_url": url,
                        "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "totals": totals,
                    }
                    results.append(game_record)
                    logging.info(f"[{team_code}] Saved totals from {url}")
                else:
                    logging.warning(f"[{team_code}] No totals found for {url}")

                if idx % SAVE_EVERY == 0:
                    progress_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

                time.sleep(random.uniform(1.5, 3.0))
            except Exception as e:
                logging.warning(f"[{team_code}] Error scraping {url}: {e}")
    finally:
        safe_quit(driver)

    # ------------------- save final results -------------------
    if results:
        progress_file.unlink(missing_ok=True)
    return results

# ---------------- ALL TEAMS SCRAPER ----------------

def scrape_all_teams():
    all_results = []

    for team_name, team_code in TEAM_MAP.items():
        logging.info(f"=== Starting {team_name} ({team_code}) ===")
        try:
            team_results = scrape_team(team_code, HEADLESS, PROXIES)
            all_results.extend(team_results)
        except Exception as e:
            logging.error(f"[{team_code}] Failed to scrape team: {e}")

    OUTPUT_FILE.write_text(json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8")
    logging.info(f"✅ Finished scraping all teams. Saved {len(all_results)} games to {OUTPUT_FILE}")

# ---------------- ENTRY ----------------

if __name__ == "__main__":
    logging.info(f"Starting full NBA {SEASON} scraper (headless).")
    scrape_all_teams()
