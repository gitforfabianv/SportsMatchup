import json
import logging
from pathlib import Path
from collections import defaultdict

# ---------- CONFIG ----------
INPUT_FILE = Path("team_totals_all_teams.json")
OUTPUT_FILE = Path("matchup_averages.json")
# ----------------------------

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def safe_float(value):
    """Convert a string to float if possible; return None otherwise."""
    try:
        v = str(value).strip()
        if v == "" or v == "-":
            return None
        return float(v)
    except Exception:
        return None


def average_matchups(games):
    """
    Group by matchup (alphabetical order of team pair) and compute stat averages.
    """
    matchups = defaultdict(lambda: defaultdict(list))

    for game in games:
        totals = game.get("totals", {})
        if len(totals) != 2:
            continue  # skip malformed entries

        teams = list(totals.keys())
        team_a, team_b = teams[0], teams[1]
        matchup_key = "_vs_".join(sorted(teams))  # e.g. "ATL_vs_BRK"

        for team, stats in totals.items():
            for stat, value in stats.items():
                val = safe_float(value)
                if val is not None:
                    matchups[matchup_key][team].append((stat, val))

    # aggregate averages
    matchup_averages = {}
    for matchup_key, team_data in matchups.items():
        avg_entry = {}
        for team, stat_pairs in team_data.items():
            stat_groups = defaultdict(list)
            for stat, val in stat_pairs:
                stat_groups[stat].append(val)
            # compute means
            avg_entry[team] = {
                stat: round(sum(vals) / len(vals), 3)
                for stat, vals in stat_groups.items()
                if vals
            }
        # count number of games in this matchup
        team_names = list(team_data.keys())
        avg_entry["games_count"] = len(
            {tuple(sorted([team_names[0], t])) for t in team_names}
        )  # optional count placeholder
        matchup_averages[matchup_key] = avg_entry

    return matchup_averages


def main():
    if not INPUT_FILE.exists():
        logging.error(f"Input file not found: {INPUT_FILE}")
        return

    logging.info(f"Loading {INPUT_FILE}...")
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    logging.info(f"Processing {len(data)} games...")
    averages = average_matchups(data)

    OUTPUT_FILE.write_text(
        json.dumps(averages, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    logging.info(f"Saved matchup averages to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
