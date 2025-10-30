# team_totals_headless_filtered.py
import json
import logging
import random
import time
from pathlib import Path
from typing import Optional, List, Dict
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------- CONFIG ----------------
TEAM = "ATL"
SEASON = 2025
OUTPUT_FILE = Path("team_totals_filtered.json")
HEADLESS = True
PROXIES: List[str] = []  # optional proxy list
PAGE_LOAD_WAIT = 12
ELEMENT_WAIT = 10
SAVE_EVERY = 1
# ----------------------------------------

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

BASE_TEAM_SCHEDULE = f"https://www.basketball-reference.com/teams/{TEAM}/{SEASON}_games.html"

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

# ---------------- PARSER ----------------

def parse_team_totals_from_html(html: str) -> Optional[Dict[str, Dict[str, str]]]:
    soup = BeautifulSoup(html, "html.parser")
    totals_per_team: Dict[str, Dict[str, str]] = {}

    for table in soup.find_all("table"):
        table_id = table.get("id", "")
        if not table_id.startswith("box-") or "-game-" not in table_id:
            continue
        team_code = table_id.split("-")[1].upper()

        # Locate "Team Totals" row
        tr = table.find("tr", {"class": None})
        for tr in table.find_all("tr"):
            th = tr.find("th", {"data-stat": "player"})
            if th and th.get_text(strip=True) == "Team Totals":
                cells = tr.find_all("td")
                headers = [
                    thd.get("data-stat") or thd.get_text(strip=True).lower()
                    for thd in table.find("thead").find_all("th")
                ]
                if team_code not in totals_per_team:
                    totals_per_team[team_code] = {}
                for i, td in enumerate(cells):
                    if i + 1 < len(headers):
                        stat_name = headers[i + 1]
                        totals_per_team[team_code][stat_name] = td.get_text(strip=True)
    return totals_per_team or None

# ---------------- MAIN FLOW ----------------

def scrape_all_games(headless: bool = HEADLESS, proxies: Optional[List[str]] = None):
    proxies = proxies or []
    results = []
    progress_file = OUTPUT_FILE.with_suffix(".progress.json")

    if progress_file.exists():
        try:
            results = json.loads(progress_file.read_text(encoding="utf-8"))
            logging.info(f"Loaded {len(results)} existing games from progress file.")
        except Exception:
            results = []

    driver = None
    try:
        driver = create_stealth_driver(headless=headless)
        logging.info("Opening schedule page...")
        driver.get(BASE_TEAM_SCHEDULE)
        WebDriverWait(driver, PAGE_LOAD_WAIT).until(
            EC.presence_of_element_located((By.ID, "games"))
        )
        links = extract_boxscore_links_from_driver(driver)
        logging.info(f"Found {len(links)} boxscore links for {TEAM}")

        for idx, url in enumerate(links, start=1):
            logging.info(f"[{idx}/{len(links)}] Visiting {url}")
            try:
                driver.get(url)
                WebDriverWait(driver, ELEMENT_WAIT).until(
                    EC.presence_of_element_located((By.XPATH, "//th[@data-stat='player' and text()='Team Totals']"))
                )
                html = driver.page_source
                totals = parse_team_totals_from_html(html)

                # NEW FILTER: keep only if target team appears
                if totals and TEAM in totals:
                    game_record = {
                        "game_url": url,
                        "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "totals": totals,
                    }
                    results.append(game_record)
                    logging.info(f"✅ Saved {TEAM} totals from {url}")
                else:
                    logging.warning(f"Skipping {url} (no {TEAM} totals found)")

                # save progress
                if idx % SAVE_EVERY == 0:
                    progress_file.write_text(
                        json.dumps(results, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )
                    logging.info(f"Progress saved ({len(results)} games).")

                time.sleep(random.uniform(1.5, 4.0))
            except Exception as e:
                logging.warning(f"Error on {url}: {e}")

    finally:
        safe_quit(driver)
        OUTPUT_FILE.write_text(
            json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        if progress_file.exists():
            try:
                progress_file.unlink()
            except Exception:
                pass
        logging.info(f"Saved {len(results)} {TEAM} games to {OUTPUT_FILE}")
        logging.info("Finished.")

# ---------------- ENTRY ----------------

if __name__ == "__main__":
    logging.info(f"Starting {TEAM} {SEASON} headless Selenium scraper (filtered).")
    scrape_all_games()
