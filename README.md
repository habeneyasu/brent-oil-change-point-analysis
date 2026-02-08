# Change Point Analysis and Statistical Modeling of Brent Oil Prices

## Project Overview

This project analyzes how major political and economic events affect Brent oil prices using Bayesian change point detection methods. The analysis identifies structural breaks in oil price time series and associates them with geopolitical events, OPEC decisions, and economic shocks.

## Project Structure

```
brent-oil-change-point-analysis/
├── data/
│   ├── raw/                    # Original dataset files
│   ├── processed/              # Cleaned and transformed data
│   └── external/               # External event data (CSV files)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_change_point_analysis.ipynb
│   └── 03_insights_generation.ipynb
├── src/
│   ├── __init__.py
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── load_data.py
│   │   └── preprocess.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── change_point_model.py
│   │   └── utils.py
│   └── visualization/
│       ├── __init__.py
│       └── plots.py
├── backend/
│   ├── app.py                  # Flask application
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── utils/
│   │   └── App.js
│   ├── package.json
│   └── README.md
├── docs/
│   ├── task1_foundation.md
│   ├── task2_analysis.md
│   └── task3_dashboard.md
├── models/                     # Saved model outputs
├── reports/                    # Generated reports and visualizations
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+ (for frontend)
- npm or yarn

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run Flask backend:
```bash
cd backend
python app.py
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## Key Dates

- Challenge Introduction: 10:30 AM UTC, Wednesday, 04 Feb 2026
- Interim Solution: 8:00 PM UTC, Sunday, 08 Feb 2026
- Final Submission: 8:00 PM UTC, Tuesday, 10 Feb 2026

## Tasks

### Task 1: Laying the Foundation for Analysis ✅

**Status**: Completed

**Deliverables**:
- ✅ Comprehensive analysis workflow document (`docs/task1_foundation.md`)
- ✅ Event data CSV with 18 key events (`data/external/key_events.csv`)
- ✅ OOP-based data processing modules with logging and exception handling
- ✅ Time series property analysis (trend, stationarity, volatility)
- ✅ Unit tests for data loading and preprocessing
- ✅ Professional visualizations
- ✅ Documentation of assumptions and limitations

**Run Task 1 Analysis**:
```bash
# Activate virtual environment
source venv/bin/activate

# Run the analysis
python run_task1.py
```

**Run Tests**:
```bash
pytest tests/ -v
```

- **Task 2**: Change Point Modeling and Insight Generation (Pending)
- **Task 3**: Developing an Interactive Dashboard (Pending)

## Team

- Tutors: Kerod, Filimon, Mahbubah
- Slack: #all-week11
- Office Hours: Mon–Fri, 08:00–15:00 UTC
