from rich.console import Console
from rich.table import Table
from player import PlayerReader, PlayerStats

def setup_table_columns(table):
    table.add_column("#", style="cyan")
    table.add_column("Released", style="cyan")
    table.add_column("Teams", style="magenta")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right", style="bold green")

def render_table(players, season, nationality):
    table = Table(
        title=f"Season {season} – players from ({nationality})",
        header_style="bold white on blue",
        title_style="bold yellow",
        show_lines=False,
        show_edge=True,
    )
    setup_table_columns(table)

    for i, p in enumerate(players, start=1):
        table.add_row(
            str(i),
            p.name,
            p.team,
            str(p.goals),
            str(p.assists),
            str(p.assists + p.goals),
        )

    console = Console()
    console.print(table)

def get_user_inputs():
    season = input("Anna kausi (esim. 2024-25): ").strip() or "2024-25"
    nationality = input("Anna maa (esim. FIN): ").strip().upper() or "FIN"
    return season, nationality


def main():
    season, nationality = get_user_inputs()

    reader = PlayerReader(season)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    if not players:
        print("No players")

    render_table(players, season, nationality)

if __name__ == "__main__":
    main()
