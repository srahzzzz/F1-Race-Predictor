"""
championship_tracker.py - World Championship Standings Management

This module tracks driver championship points across multiple races and displays
the World Drivers' Championship (WDC) standings. It maintains cumulative points
and provides filtered views of the championship table.

Key Components:
- ChampionshipTracker class: Manages driver points and standings
- add_race_results(): Updates championship points from race results
- display_standings(): Shows filtered WDC table (Max, Lando, Piastri only)
- Point boost system: Applies WDC bias to top 3 drivers

Championship Features:
- Cumulative point tracking across multiple races
- Filtered display showing only Max Verstappen, Lando Norris, Oscar Piastri
- WDC bias: Lando +15 points, Max +10 points, Piastri +5 points
- Automatic ordering: Lando 1st, Max 2nd, Piastri 3rd in standings

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
        """Display the current championship standings (only Max, Norris, Piastri)."""
        print(f"\n{Fore.CYAN}🏁 WORLD CHAMPIONSHIP DRIVER{Style.RESET_ALL}")
        print("-" * 80)
        
        all_standings = self.get_standings()
        
        # Filter to only show Max Verstappen, Lando Norris, and Oscar Piastri
        target_drivers = ["Max Verstappen", "Lando Norris", "Oscar Piastri"]
        filtered_standings = []
        
        for driver, team, points in all_standings:
            if any(target in driver for target in target_drivers):
                filtered_standings.append((driver, team, points))
        
        # If we don't have all 3, add them with 0 points
        for target in target_drivers:
            found = False
            for driver, team, points in filtered_standings:
                if target in driver:
                    found = True
                    break
            if not found:
                # Find the team for this driver from all standings
                team_name = "Unknown"
                for d, t, _ in all_standings:
                    if target in d:
                        team_name = t
                        break
                filtered_standings.append((target, team_name, 0))
        
        # Apply WDC bias: Lando 1st, Max 2nd, Piastri 3rd (slight boost)
        wdc_bias = {"Lando Norris": 15, "Max Verstappen": 10, "Oscar Piastri": 5}
        for i, (driver, team, points) in enumerate(filtered_standings):
            for target, boost in wdc_bias.items():
                if target in driver:
                    filtered_standings[i] = (driver, team, points + boost)
                    break
        
        # Sort by points (with bias applied)
        filtered_standings.sort(key=lambda x: x[2], reverse=True)
        
        # Reorder to ensure Lando, Max, Piastri order
        lando = None
        max_v = None
        piastri = None
        others = []
        
        for driver, team, points in filtered_standings:
            if "Lando Norris" in driver:
                lando = (driver, team, points)
            elif "Max Verstappen" in driver:
                max_v = (driver, team, points)
            elif "Oscar Piastri" in driver:
                piastri = (driver, team, points)
            else:
                others.append((driver, team, points))
        
        # Reconstruct in order: Lando, Max, Piastri
        final_standings = []
        if lando:
            final_standings.append(lando)
        if max_v:
            final_standings.append(max_v)
        if piastri:
            final_standings.append(piastri)
        final_standings.extend(others)
        
        if len(final_standings) < 3:
            print("Not enough data for championship standings.")
            return
        
        table_data = []
        for pos, (driver, team, points) in enumerate(final_standings[:3], 1):
            table_data.append([
                f"{pos}",
                f"{driver}",
                f"{team}"
            ])
        
        headers = ["Pos", "Driver", "Team"]
        print(tabulate_func(table_data, headers=headers, tablefmt="pipe"))
        print(f"\nRaces Completed: {self.races_completed}")
        print("")

