import click
from nba_api.api import get_teams, fetch_team_details
from nba_api.teams_static import get_nba_teams
from nba_api.matchups import get_matchup_data
from nba_api.scrapers import scrape_team_wikipedia_data 
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout

console = Console()

# Function to display matchup
def display_matchup(team1, team2, use_scrape, use_pull):
    def teams_func():
        return get_teams(use_scrape=use_scrape, use_pull=use_pull)

    result, status = get_matchup_data(team1, team2, teams_func, fetch_team_details)

    if status != 200:
        console.print(result.get("error", "Unknown error."), style="bold red")
        return

    team1_details = result['team1']
    team2_details = result['team2']

    # Your existing code for printing with panels, layouts etc.
    team1_panel = Panel(
        Text(
            f"**Location:** {team1_details.get('location', 'N/A')}\n"
            f"**Team Name:** {team1_details.get('team_name', 'N/A')}\n"
            f"**Seasons:** {team1_details.get('seasons', 'N/A')}\n"
            f"**Record:** {team1_details.get('record', 'N/A')}\n"
            f"**Playoff Appearances:** {team1_details.get('playoff_appearances', 'N/A')}\n"
            f"**Championships:** {team1_details.get('championships', 'N/A')}\n",
            style="bold green"
        ),
        title=team1,
        border_style="green"
    )

    team2_panel = Panel(
        Text(
            f"**Location:** {team2_details.get('location', 'N/A')}\n"
            f"**Team Name:** {team2_details.get('team_name', 'N/A')}\n"
            f"**Seasons:** {team2_details.get('seasons', 'N/A')}\n"
            f"**Record:** {team2_details.get('record', 'N/A')}\n"
            f"**Playoff Appearances:** {team2_details.get('playoff_appearances', 'N/A')}\n"
            f"**Championships:** {team2_details.get('championships', 'N/A')}\n",
            style="bold green"
        ),
        title=team2,
        border_style="blue"
    )

    layout = Layout()
    layout.split(Layout(name="matchup"))
    layout["matchup"].split_row(Layout(team1_panel), Layout(team2_panel))

    console.print(layout)

# Function to display a DataFrame in a rich Table and exclude unnecessary columns
def display_dataframe(df):
    print(f"Displaying DataFrame: {df}")
    required_columns = ['franchise', 'AGE', 'conference', 'championships_won']
    if all(col in df.columns for col in required_columns):
        df = df[required_columns]
        table = Table(show_header=True, header_style="bold magenta")
        for col in df.columns:
            table.add_column(col, justify="left", style="cyan", no_wrap=True)
        for _, row in df.iterrows():
            table.add_row(*map(str, row.values))
        console.print(table)
    else:
        console.print("Data does not contain required columns.", style="bold red")

# Function to display credits
def display_credits():
    credits_content = """
CREDITS

Please consider sponsoring me or buying me a coffee if you get value from my work.

Sponsor: https://github.com/sponsors/tedleyem

Coffee: https://buymeacoffee.com/techdadteddy
"""
    panel = Panel(Text(credits_content, justify="center"), border_style="orange1")
    console.print(panel)

# CLI entry point
@click.command(
    help="Pull NBA team data and get team info for matching up teams.\n"
         "Options:\n"
         "  --test-api: Test the API call\n"
         "  --teams: Get teams list\n"
         "  --team1 and --team2: Choose two teams for matchups comparison\n"
         "  --team-details: Get details for a specific team by its franchise name\n"
         "  --scrape: Use web scraping for fetching data\n"
         "  --pull: Use RapidAPI for fetching data\n"
         "  --credits: Display credits"
)
@click.option('--test-api', is_flag=True, help="Test the API call")
@click.option('--teams', is_flag=True, help="Get teams list")
@click.option('--team', type=str, help="Scrape Wikipedia data for a specific team short name (e.g. 'MIA')")
@click.option('--team1', type=str, help="Choose team 1 for matchups comparison")
@click.option('--team2', type=str, help="Choose team 2 for matchups comparison")
@click.option('--team-details', type=str, help="Get details for a specific team by its franchise name")
@click.option('--scrape', is_flag=True, help="Use web scraping for fetching data")
@click.option('--pull', is_flag=True, help="Use RapidAPI for fetching data")
@click.option('--credits', is_flag=True, help="Display credits")
def cli(test_api, team, teams, team1, team2, team_details, scrape, pull, credits):
    if credits:
        # Display credits
        display_credits()
        return

    layout = Layout()
    
    # Titles and Notes Panel
    title_panel = Panel(
        Text("NBA Matchups", justify="center", style="bold yellow")
    )
    note_content = Text(
        "Pull NBA team data and get team info for matching up teams.\n"
        "--teams Get teams list\n"
        "--help for more options",
        style="white",
        justify="center"
    )
    note_panel = Panel(note_content, border_style="orange1")
    
    footer_content = Text(
        f"Github: https://github.com/tedleyem\n",
        style="white",
        justify="center"
    )
    footer_panel = Panel(footer_content, border_style="green")

    # Split layout into title, note, content, and footer panels
    layout.split(
        Layout(title_panel, name="title", size=3),
        Layout(note_panel, name="note", size=6),
        Layout(name="content"),
        Layout(footer_panel, name="footer", size=3)
    )

    if test_api:
        # Test API call using RapidAPI pull
        teams_list = get_teams(use_scrape=False, use_pull=True)
        layout['content'].update(Panel(f"API call successful. Found {len(teams_list)} teams using RapidAPI (pull).", border_style="green"))

    elif team:
        # Scrape Wikipedia using short_name like 'MIA'
        teams = get_nba_teams()
        match = next((t for t in teams if t['short_name'] == team.upper()), None)

        if not match:
            layout['content'].update(Panel(f"Team with short name '{team}' not found.", border_style="red"))
        else:
            team_data = scrape_team_wikipedia_data(match['name'])

            if not team_data:
                layout['content'].update(Panel("Could not fetch Wikipedia data.", border_style="red"))
            else:
                info = "\n".join([f"[bold]{key}:[/bold] {value}" for key, value in team_data.items()])
                layout['content'].update(Panel(Text(info), title=match['name'], border_style="blue"))

    elif teams:
        # Get teams list and display in a pretty box using pandas and rich
        teams_list = get_teams(use_scrape=scrape, use_pull=pull)
        if teams_list:
            df = pd.DataFrame(teams_list)
            display_dataframe(df)

    elif team1 and team2:
        display_matchup(team1, team2, scrape, pull)

    elif team_details:
        details = fetch_team_details(team_details)
        if details:
            df = pd.DataFrame([details])
            display_dataframe(df)
        else:
            layout['content'].update(Panel("No details found for the specified team ID.", border_style="red"))

    else:
        # Default action: Display Miami Heat and Minnesota Timberwolves comparison
        print("Fetching default team comparison MIA vs MIN...")
        display_matchup("Miami Heat", "Minnesota Timberwolves", scrape, pull)

    console.print(layout)

if __name__ == "__main__":
    cli()