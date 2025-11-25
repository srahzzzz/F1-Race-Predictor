"""
Minimal visualization helpers for displaying race results in the console.
"""

from tabulate import tabulate as tabulate_func
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init()


def display_qualifying_results(qualifying_results):
    """Display the qualifying results in a formatted table."""
    print(f"\n{Fore.YELLOW}QUALIFYING RESULTS{Style.RESET_ALL}")
    print("-" * 60)

    table_data = []
    for i, driver in enumerate(qualifying_results, 1):
        table_data.append([
            f"{i:2d}",
            f"{driver.name}",
            f"{driver.team}"
        ])

    headers = ["Pos", "Driver", "Team"]
    print(tabulate_func(table_data, headers=headers, tablefmt="pipe"))
    print("")


def display_race_results(results):
    """Display the race results in a formatted table."""
    print(f"\n{Fore.GREEN}RACE RESULTS{Style.RESET_ALL}")
    print("-" * 80)

    table_data = []
    for result in results:
        status = result.status
        if status == "Finished":
            time_display = format_race_time(result.time)
        else:
            time_display = f"{Fore.RED}{status}{Style.RESET_ALL}"

        table_data.append([
            f"{result.finishing_position:2d}",
            f"{result.driver.name}",
            f"{result.driver.team}",
            time_display,
            f"{result.points}" if result.points > 0 else ""
        ])

    headers = ["Pos", "Driver", "Team", "Time/Status", "Pts"]
    print(tabulate_func(table_data, headers=headers, tablefmt="pipe"))


def display_podium(results, track):
    """Display the podium (top 3) in a formatted table."""
    print(f"\n{Fore.MAGENTA}🏆 PODIUM FOR {track.name.upper()} 2025{Style.RESET_ALL}")
    print("-" * 80)
    
    # Get top 3 finished drivers
    podium = [r for r in results if r.status == "Finished"][:3]
    
    if len(podium) < 3:
        print("Not enough finishers for a complete podium.")
        return
    
    table_data = []
    for result in podium:
        time_display = format_race_time(result.time)
        table_data.append([
            f"{result.finishing_position}",
            f"{result.driver.name}",
            f"{result.driver.team}",
            time_display,
            f"{result.points}"
        ])
    
    headers = ["Pos", "Driver", "Team", "Time", "Pts"]
    print(tabulate_func(table_data, headers=headers, tablefmt="pipe"))
    print("")


def format_race_time(seconds):
    """Format race time in minutes:seconds.milliseconds format."""
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02d}:{remaining_seconds:02d}.{milliseconds:03d}"


