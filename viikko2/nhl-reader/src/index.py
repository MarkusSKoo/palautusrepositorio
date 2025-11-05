from player import PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table

def render_table(players, season, nationality):
    table = Table(
        title=f"Season {season} – players from ({nationality})",
        header_style="bold white on blue",
        title_style="bold yellow",
        show_lines=False,
        show_edge=True,
        pad_edge=True
    )
    table.add_column("#", justify="right", style="bold")
    table.add_column("Released", style="cyan")
    table.add_column("Teams", style="magenta")
    table.add_column("Games", justify="right")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right", style="bold green")

    for i, p in enumerate(players, start=1):
        table.add_row(
            str(i),
            p.name,
            p.team,
            str(p.games),
            str(p.goals),
            str(p.assists),
            str(p.points),
        )

    console = Console()
    console.print(table)

def main():
    # Kysy käyttäjältä kausi ja maa
    season = input("Anna kausi (esim. 2024-25): ").strip() or "2024-25"
    nationality = input("Anna maa (esim. FIN): ").strip().upper() or "FIN"

    try:
        reader = PlayerReader(season)
    except Exception as e:
        Console().print(f"[red]Datan haku epäonnistui:[/red] {e}")
        return

    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    if not players:
        Console().print(f"[yellow]Ei pelaajia maalle {nationality} kaudella {season}.[/yellow]")
        return

    render_table(players, season, nationality)

if __name__ == "__main__":
    main()
