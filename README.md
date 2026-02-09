# Brent Oil Change Point Analysis

> **Detecting structural breaks in oil prices and quantifying the impact of geopolitical events using Bayesian inference**

This project employs Bayesian change point detection to identify when and how major political and economic events cause structural shifts in Brent crude oil prices. Using PyMC and MCMC methods, we quantify the causal impact of events like OPEC decisions, geopolitical conflicts, and economic crises on global oil markets.

## 🎯 Key Features

- **Bayesian Change Point Detection**: PyMC-based model identifying structural breaks in price dynamics
- **Event Association**: Links detected change points with 18+ key geopolitical and economic events
- **Impact Quantification**: Probabilistic statements about price changes (e.g., "Following OPEC production cut, prices increased by X%")
- **Production-Ready Codebase**: OOP design, comprehensive logging, exception handling, and unit tests
- **Interactive Dashboard**: Flask backend + React frontend (Task 3)

## 📊 Project Status

| Task | Status | Deliverables |
|------|--------|-------------|
| **Task 1** | ✅ Complete | Workflow documentation, event data (18 events), EDA, visualizations |
| **Task 2** | ✅ Complete | Bayesian model, MCMC sampling, convergence checks, event association, impact quantification |
| **Task 3** | 🚧 In Progress | Interactive dashboard (Flask + React) |

## 🚀 Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run Task 1: Foundation Analysis
python notebooks/01_task1_foundation_analysis.py

# Run Task 2: Change Point Detection
python notebooks/02b_build_change_point_model.py
python notebooks/02c_interpret_model_output.py
python notebooks/02d_associate_events.py

# Run Tests
pytest tests/ -v
```

## 📁 Project Structure

```
brent-oil-change-point-analysis/
├── data/
│   ├── raw/              # Brent oil price dataset
│   ├── processed/        # Cleaned data
│   └── external/         # Event data (18 key events)
├── src/                  # Core modules
│   ├── data_processing/  # Data loading & preprocessing
│   ├── models/           # Bayesian change point models
│   └── visualization/    # Plotting utilities
├── notebooks/            # Analysis scripts
├── backend/              # Flask API (Task 3)
├── frontend/             # React dashboard (Task 3)
├── docs/                 # Documentation
└── reports/              # Generated visualizations & results
```

## 🔬 Methodology

1. **Data Preparation**: Load 35 years of daily Brent prices (1987-2022), compute log returns
2. **Bayesian Modeling**: PyMC change point model with discrete uniform prior on τ (change point location)
3. **MCMC Sampling**: 4 chains, 2000 draws per chain, convergence diagnostics (R-hat < 1.01)
4. **Event Association**: Match change points with events within 90-day window
5. **Impact Quantification**: Probabilistic statements with credible intervals

## 📈 Key Results

- **Change Point Detection**: Identifies structural breaks with uncertainty quantification
- **Event Correlation**: Associates change points with OPEC decisions, conflicts, crises
- **Impact Measurement**: Quantifies price changes in USD and percentage terms
- **Visualizations**: Trace plots, posterior distributions, event overlays

## 🛠️ Technology Stack

- **Python**: pandas, numpy, PyMC, ArviZ, statsmodels
- **Visualization**: matplotlib, seaborn
- **Backend**: Flask, Flask-CORS
- **Frontend**: React, Recharts
- **Testing**: pytest

## 📚 Documentation

- **[Task 1 Foundation](docs/task1_foundation.md)**: Analysis workflow, assumptions, limitations
- **[Task 2 Analysis](docs/task2_analysis.md)**: Change point modeling and results
- **[Advanced Extensions](docs/advanced_extensions.md)**: VAR models, Markov-Switching, multi-factor approaches


**Challenge Dates**: Feb 4-10, 2026 | **Status**: Task 1 & 2 Complete ✅
