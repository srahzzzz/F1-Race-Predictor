"""
weather_model.py - Weather Condition Generation and Simulation

This module generates realistic weather conditions for Formula 1 races based on
track location, season, and historical weather patterns. Weather significantly
impacts race strategy, tire selection, and driver performance.

Key Components:
- WeatherCondition dataclass: Represents weather state (dry/wet/mixed, temperature, humidity)
- generate_weather() function: Creates realistic weather based on track and date
- Location-based adjustments: Different probabilities for different regions
- Season-based temperature and rain probability calculations

Weather Generation Logic:
- Location-based probabilities: Arid regions (Qatar, UAE) have 95% dry probability
- Season adjustments: Spring/autumn months have higher rain probability
- Temperature calculations: Based on month, location, and seasonal patterns
- Rain intensity: Scales from 0 (dry) to 10 (monsoon) for wet conditions

Integration:
- Used by app.py to automatically generate weather for each race
- Referenced by base_race_model.py for weather impact calculations
- Uses track_data.py for location and date information

Special Features:
- Arid track handling: Qatar, Bahrain, Saudi Arabia, UAE, Las Vegas forced to 95% dry
- Losail-specific: 95% dry, 3% wet, 2% mixed (extremely rare rain)
- Automatic month extraction from track date strings
"""

import random

from dataclasses import dataclass


@dataclass
class WeatherCondition:
    """Represents weather conditions during a race."""
    condition: str  # 'dry', 'wet', 'mixed'
    temperature: float  # in Celsius
    humidity: float  # percentage
    wind_speed: float  # km/h
    rain_chance: float  # percentage chance of rain
    rain_intensity: float  # 0-10 scale, 0 is no rain, 10 is monsoon
    track_temperature: float  # in Celsius
    
    def __str__(self):
        return f"{self.condition.title()} - {self.temperature}°C, Rain: {int(self.rain_chance)}%"
    
    @property
    def is_wet(self):
        """Check if conditions are wet."""
        return self.condition == 'wet' or (self.condition == 'mixed' and self.rain_intensity > 3)

    @property
    def weather_factor(self):
        """Calculate impact of weather on race conditions.
        Returns a value between 0-1, where 0 is extreme weather impact, 1 is ideal conditions.
        """
        if self.condition == 'dry':
            # Perfect conditions
            if 18 <= self.temperature <= 26 and self.wind_speed < 20:
                return 1.0
            # Very hot or windy
            elif self.temperature > 35 or self.wind_speed > 40:
                return 0.85
            # Cold
            elif self.temperature < 10:
                return 0.9
            # Normal
            else:
                return 0.95
        elif self.condition == 'wet':
            # Heavy rain
            if self.rain_intensity > 7:
                return 0.6
            # Medium rain
            elif 4 <= self.rain_intensity <= 7:
                return 0.7
            # Light rain
            else:
                return 0.8
        else:  # mixed
            # Changing conditions
            base = 0.85
            rain_factor = 0.1 * self.rain_intensity / 10
            return base - rain_factor


def generate_weather(track, month=None, forced_condition=None):
    """Generate realistic weather conditions for a given track.
    
    Args:
        track: Track object
        month: Optional month to override track date
        forced_condition: Optional weather condition to force ('dry', 'wet', 'mixed')
        
    Returns:
        WeatherCondition object
    """
    if month is None:
        # Extract month from track date
        import datetime
        import re
        
        # Handle date format like "April 4-6, 2025"
        # Extract just the month name using regex
        month_match = re.match(r'(\w+)\s+\d+', track.date)
        if month_match:
            month_name = month_match.group(1)
            # Convert month name to month number
            month_dict = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            month = month_dict.get(month_name, datetime.datetime.now().month)
        else:
            # Fallback to current month if parsing fails
            month = datetime.datetime.now().month
    
    # Weather probabilities based on location and month
    if forced_condition:
        condition = forced_condition
    else:
        # Default probabilities
        dry_prob = 0.7
        wet_prob = 0.2
        mixed_prob = 0.1
        
        country = track.country.lower()
        track_name = track.name.lower()
        
        # Adjust for certain tracks/seasons known for rain
        if country in ["malaysia", "japan", "brazil", "belgium", "great britain", "singapore"]:
            dry_prob -= 0.2
            wet_prob += 0.1
            mixed_prob += 0.1
        
        # Extremely arid venues (Qatar, Bahrain, Saudi Arabia, UAE, Las Vegas)
        # should almost never be wet unless the user explicitly forces it.
        arid_locations = ["qatar", "bahrain", "saudi arabia", "uae", "united arab emirates", "las vegas"]
        if any(loc in country or loc in track_name for loc in arid_locations):
            dry_prob = 0.9
            wet_prob = 0.05
            mixed_prob = 0.05
        
        # Specifically handle Losail/Lusail where rain is exceptionally rare.
        if "losail" in track_name or "lusail" in track_name:
            dry_prob = 0.95
            wet_prob = 0.03
            mixed_prob = 0.02
            
        # Adjust for season (more rain in certain months)
        if month in [3, 4, 10, 11]:  # Spring and autumn months
            dry_prob -= 0.1
            wet_prob += 0.05
            mixed_prob += 0.05
            
        # Choose condition based on probabilities
        conditions = ['dry', 'wet', 'mixed']
        probabilities = [dry_prob, wet_prob, mixed_prob]
        condition = random.choices(conditions, weights=probabilities, k=1)[0]
    
    # Base temperature on month and location
    base_temp = 22  # Default base temperature
    
    # Adjust for season
    season_adj = {
        1: -5, 2: -4, 3: -2, 4: 0,     # Winter/Spring
        5: 3, 6: 5, 7: 7, 8: 7,        # Summer
        9: 4, 10: 0, 11: -3, 12: -5    # Autumn/Winter
    }
    
    # Adjust for location (rough approximations)
    location_adj = 0
    if track.country.lower() in ["bahrain", "saudi arabia", "qatar", "uae", "singapore"]:
        location_adj = 8  # Hot locations
    elif track.country.lower() in ["canada", "japan", "great britain", "belgium"]:
        location_adj = -3  # Cooler locations
        
    # Calculate temperature with some randomness
    temp_base = base_temp + season_adj[month] + location_adj
    temperature = round(temp_base + random.uniform(-3, 3), 1)
    
    # Generate other weather parameters
    if condition == 'dry':
        humidity = random.uniform(40, 70)
        wind_speed = random.uniform(0, 25)
        rain_chance = random.uniform(0, 15)
        rain_intensity = 0
        track_temp = temperature + random.uniform(10, 20)
    elif condition == 'wet':
        humidity = random.uniform(70, 95)
        wind_speed = random.uniform(5, 40)
        rain_chance = random.uniform(70, 100)
        rain_intensity = random.uniform(3, 10)
        track_temp = temperature + random.uniform(0, 7)
    else:  # mixed
        humidity = random.uniform(60, 85)
        wind_speed = random.uniform(3, 35)
        rain_chance = random.uniform(40, 80)
        rain_intensity = random.uniform(1, 6)
        track_temp = temperature + random.uniform(5, 15)
        
    return WeatherCondition(
        condition=condition,
        temperature=round(temperature, 1),
        humidity=round(humidity, 1),
        wind_speed=round(wind_speed, 1),
        rain_chance=round(rain_chance, 1),
        rain_intensity=round(rain_intensity, 1),
        track_temperature=round(track_temp, 1)
    )