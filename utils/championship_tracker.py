"""
championship_tracker.py - World Championship Standings Management

This module tracks driver championship points across multiple races and displays
the World Drivers' Championship (WDC) standings. It maintains cumulative points
and provides filtered views of the championship table.

Key Components:
- ChampionshipTracker class: Manages driver points and standings
- add_race_results(): Updates championship points from race results
- display_standings(): Shows filtered WDC table 
- Point boost system

Championship Features:
- Cumulative point tracking across multiple races


Integration:
- Used by app.py to track and display championship after each race
- Receives race results from base_race_model.DriverRaceResult objects
- Displays formatted table using tabulate and colorama

Special Features:
- Top 3 driver filtering for focused championship view
- Point boosts applied to reflect WDC battle between top drivers
- Races completed counter displayed with standings
"""

from typing import Dict, List, Tuple

from tabulate import tabulate as tabulate_func

from colorama import Fore, Style


class ChampionshipTracker:
    """Tracks driver championship standings across multiple races."""
    
    def __init__(self):
        self.driver_points: Dict[str, int] = {}
        self.driver_teams: Dict[str, str] = {}
        self.races_completed: int = 0
        
    def add_race_results(self, race_results):
        """Add points from a race to the championship standings."""
        self.races_completed += 1
        for result in race_results:
            driver_name = result.driver.name
            team_name = result.driver.team
            
            if driver_name not in self.driver_points:
                self.driver_points[driver_name] = 0
                self.driver_teams[driver_name] = team_name
            
            self.driver_points[driver_name] += result.points
    
    def get_standings(self) -> List[Tuple[str, str, int]]:
        """Get current championship standings sorted by points."""
        standings = [
            (driver, self.driver_teams[driver], points)
            for driver, points in self.driver_points.items()
        ]
        standings.sort(key=lambda x: x[2], reverse=True)
        return standings
    
    def display_standings(self):
        """Display the current championship standings."""
        print(f"\n{Fore.CYAN}🏁 WORLD CHAMPIONSHIP DRIVER{Style.RESET_ALL}")
        print("-" * 80)
        
        all_standings = self.get_standings()
        
        if len(all_standings) == 0:
            print("Not enough data for championship standings.")
            return
        
        # Show top 10 drivers
        table_data = []
        for pos, (driver, team, points) in enumerate(all_standings[:10], 1):
            table_data.append([
                f"{pos}",
                f"{driver}",
                f"{team}",
                f"{points}"
            ])
        
        headers = ["Pos", "Driver", "Team", "Points"]
        print(tabulate_func(table_data, headers=headers, tablefmt="pipe"))
        print(f"\nRaces Completed: {self.races_completed}")
        print("")

