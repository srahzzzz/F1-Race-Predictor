# 🏎️ Formula 1 Race Predictor 2025

This is a Formula 1 race simulation tool that combines **real F1 data** to predict race outcomes for the 2025 F1 season. The simulator integrates live Formula 1 telemetry data, driver performance statistics, and team analytics to provide realistic race predictions.


---

## ✨ Overview

This simulator models complete F1 race weekends with qualifying sessions and full race simulations. It uses real Formula 1 data from the Fast-F1 API (a python package for accessing Formula 1 results, schedules, timing data and telemetry)

### Key Highlights

- 🏁 **Real F1 Data Integration**: Fetches actual driver and team performance data from Fast-F1 API
- 🎯 **Focused Simulation**: Streamlined output showing only essential race information
- 📊 **Championship Tracking**: Tracks World Drivers' Championship standings across races
- 🌦️ **Realistic Weather**: Location-based weather generation with arid track handling
- 🏆 **Performance Modeling**: Advanced algorithms with driver skill, car performance, and track characteristics

---

## 🚀 Features

### Core Simulation Features

- **Real F1 Data Enhancement**
  - Historical driver performance metrics from 2022-2024 seasons
  - Team reliability and car performance data
  - Track-specific lap times and weather patterns
  - Weighted blending of real data (70%) with simulation data (30%)

- **Championship Standings**
  - Cumulative point tracking across multiple races
  - World Drivers' Championship table

- **Focused Output Display**
  - Qualifying results table
  - Race results with positions, times, and points
  - Podium finishers (top 3) with race name and year
  - Championship standings filtered to top contenders

---

## 🏁 Improvements (Planned)

- Improve weather realism (dynamic conditions, track evolution)
- Introduce tyre wear, pit strategies, and safety cars
- Add constructor standings and enhanced championship tracking
- Implement mechanical failures + DNF logic
- Add simple UI/visualization for results
- Explore ML-based performance prediction
- Enable exporting race reports (CSV/PDF)

---

## 🔧 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/srahzzzz/F1-Race-Predictor.git
cd F1-Race-Predictor
```

### Step 2: Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

Install all required packages using the dependencies file:
```bash
pip install -r dependencies.txt
```

### Step 4: Run the Application

```bash
python app.py
```

**Made by Sarah Nauman**

*Please reach me at sarahnauman15@gmail.com — unless it's about why Max keeps winning in my predictor (in that case please contact Red Bull instead 🏎️💔)*
