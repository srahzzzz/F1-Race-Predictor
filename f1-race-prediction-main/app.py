"""
Formula 1 Race Prediction Simulator
Main page
"""

import os
import sys
from tabulate import tabulate as tabulate_func

# Setup comprehensive Fast-F1 logging suppression before any other imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
from ui_loading import setup_global_logging_suppression
setup_global_logging_suppression()

# Import our data models
from data.driver_data import get_all_drivers
from data.team_data import get_all_teams
from data.track_data import get_calendar
from data.data_integration import real_data_enhancer

# Import our simulation models
from models.advanced_race_model import create_enhanced_simulator
from models.weather_model import generate_weather

# Import visualization utilities
from utils.race_visualization import (
    display_qualifying_results, display_race_results, display_podium
)
from utils.ui_loading import loading_with_animation
from utils.championship_tracker import ChampionshipTracker

# Global championship tracker
championship_tracker = ChampionshipTracker()


def print_welcome():
    """Print welcome message with app information."""
    print("\n" + "=" * 80)
    print("🏎️  FORMULA 1 RACE PREDICTION SIMULATOR — 2025 SEASON  🏁")
    print("=" * 80)
    print("\nA fast-paced simulator that predicts fictional F1 race outcomes, with")
    print("real-time performance modeling and championship standings tracking.")
    print("\n" + "=" * 80 + "\n")


def select_track():
    """Prompt user to select a track from the 2025 calendar."""
    all_tracks = get_calendar()
    
    # Filter to only show Qatar and Abu Dhabi
    tracks = [t for t in all_tracks if "Qatar" in t.name or "Abu Dhabi" in t.name or "Losail" in t.name or "Yas Marina" in t.name]
    
    print("\nAvailable races left in the 2025 F1 Calendar:")
    print("-" * 60)
    
    table_data = []
    for i, track in enumerate(tracks, 1):
        table_data.append([i, track.name, track.country, track.date])
    
    headers = ["Option", "Circuit", "Country", "Race Date"]
    print(tabulate_func(table_data, headers=headers, tablefmt="pipe"))
    
    while True:
        try:
            choice = input("\nSelect a race by number (or 'q' to quit): ")
            if choice.lower() == 'q':
                sys.exit(0)
                
            choice = int(choice)
            if 1 <= choice <= len(tracks):
                return tracks[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(tracks)}")
        except ValueError:
            print("Please enter a valid number")


def fetch_realistic_weather(track):
    """Automatically generate realistic weather without user prompts."""
    return generate_weather(track)


def run_race_simulation(track, weather_option):
    """Run the complete race simulation with real F1 data integration."""
    # Get all drivers and teams
    drivers = get_all_drivers()
    teams = get_all_teams()
    
    # Enhance with real F1 data (silently)
    try:
        enhanced_drivers, enhanced_teams = loading_with_animation(
            "",
            lambda: real_data_enhancer.enhance_race_prediction(drivers, teams, track)
        )
    except Exception:
        enhanced_drivers, enhanced_teams = drivers, teams
    
    # Create enhanced race simulator with real data
    weather = weather_option
    simulator = create_enhanced_simulator(track, enhanced_drivers, enhanced_teams, weather, real_data_enhancer)
    
    # Simulate qualifying (silently)
    qualifying_results = simulator.simulate_qualifying()
    
    # Simulate race (silently)
    race_results = simulator.simulate_race()
    
    # Apply Qatar-specific bias: Max, Lando, Piastri
    if "Qatar" in track.name or "Losail" in track.name:
        # Find the three drivers
        max_verstappen = None
        lando_norris = None
        oscar_piastri = None
        
        for result in race_results:
            if "Verstappen" in result.driver.name:
                max_verstappen = result
            elif "Norris" in result.driver.name:
                lando_norris = result
            elif "Piastri" in result.driver.name:
                oscar_piastri = result
        
        # Reorder to Max 1st, Lando 2nd, Piastri 3rd (if they finished)
        if max_verstappen and max_verstappen.status == "Finished":
            race_results.remove(max_verstappen)
            race_results.insert(0, max_verstappen)
            max_verstappen.finishing_position = 1
            max_verstappen.points = 25
        
        if lando_norris and lando_norris.status == "Finished":
            race_results.remove(lando_norris)
            # Insert after Max if he exists, otherwise at position 0
            insert_pos = 1 if max_verstappen and max_verstappen.status == "Finished" else 0
            race_results.insert(insert_pos, lando_norris)
            lando_norris.finishing_position = 2
            lando_norris.points = 18
        
        if oscar_piastri and oscar_piastri.status == "Finished":
            race_results.remove(oscar_piastri)
            # Insert after Lando
            insert_pos = 2 if (max_verstappen and max_verstappen.status == "Finished" and 
                              lando_norris and lando_norris.status == "Finished") else 1
            race_results.insert(insert_pos, oscar_piastri)
            oscar_piastri.finishing_position = 3
            oscar_piastri.points = 15
        
        # Reassign positions for remaining drivers
        for i, result in enumerate(race_results[3:], start=4):
            result.finishing_position = i
    
    # Display results
    display_qualifying_results(qualifying_results)
    display_race_results(race_results)
    display_podium(race_results, track)
    
    # Update championship standings
    championship_tracker.add_race_results(race_results)
    championship_tracker.display_standings()


def show_analysis_menu():
    """Provide a minimal menu for continuing or exiting."""
    while True:
        print("\nNext Actions:")
        print("1. Simulate another race")
        print("2. Quit")
        
        try:
            choice = input("\nSelect an option (1-2): ")
            choice = int(choice)
            
            if choice == 1:
                return True
                
            elif choice == 2:
                return False
                
            else:
                print("Please enter 1 or 2")
                
        except ValueError:
            print("Please enter a valid number")


def main():
    """Main application entry point."""
    print_welcome()
    
    while True:
        try:
            # Let user select track
            track = select_track()
            
            # Automatically fetch realistic weather conditions
            weather = fetch_realistic_weather(track)
            
            # Run simulation
            run_race_simulation(track, weather)
            
            # Show analysis menu
            continue_simulation = show_analysis_menu()
            if not continue_simulation:
                break
                
        except KeyboardInterrupt:
            print("\nExiting application...")
            break
            
    print("\nThank you for using the F1 Race Prediction Simulator!")


if __name__ == "__main__":
    # Check for required packages
    try:
        import tabulate
        import colorama
    except ImportError:
        print("Missing required packages. Installing dependencies...")
        import subprocess
        subprocess.call([sys.executable, "-m", "pip", "install", 
                        "tabulate", "colorama"])
        print("Dependencies installed. Starting application...")
    
    main()