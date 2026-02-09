
## Business Objective

**Birhan Energies** is a consultancy firm specializing in data-driven insights for the energy sector. This analysis addresses how major political and economic events (political decisions, conflicts in oil-producing regions, international sanctions, OPEC policy changes) affect Brent oil prices. **Stakeholders** include investors (risk management, forecasting), policymakers (economic stability, energy security), and energy companies (operational planning, cost control). The goal is to identify structural breaks in price time series and associate them with events to enable better decision-making in the volatile oil market.

---

## Data Analysis Workflow

Our 8-step workflow: (1) Data loading and validation (1987-2022 daily prices), (2) Preprocessing (date parsing, log returns), (3) Exploratory data analysis (visualization, trend, stationarity, volatility), (4) Event data compilation (18 key events), (5) Bayesian change point modeling (PyMC, MCMC), (6) Change point detection (identify dates, quantify parameters), (7) Impact quantification (price changes, percentages), (8) Insight generation (dashboard, report). **Key Processes**: ADF/KPSS stationarity tests, rolling volatility analysis, Bayesian inference with PyMC.

---

## Event Data Compilation

**18 key events** (1990-2022) compiled in `data/external/key_events.csv`. **Distribution**: 13 High-impact, 5 Medium-impact events across Middle East (33%), Global (44%), Asia (11%), Europe (6%), North America (6%). **Visualization**: Price time series with event markers (see `reports/price_with_events.png`) shows potential associations between events and price movements.

**Key Events Summary**:

| Date | Event | Region | Impact |
|------|-------|--------|--------|
| 1990-08-02 | Iraq invades Kuwait - Gulf War | Middle East | High |
| 1998-12-01 | Asian Financial Crisis | Asia | High |
| 2001-09-11 | 9/11 Attacks | Global | High |
| 2003-03-20 | Iraq War Begins | Middle East | High |
| 2008-09-15 | Global Financial Crisis | Global | High |
| 2014-11-27 | OPEC no production cut decision | Global | High |
| 2020-01-01 | COVID-19 Pandemic | Global | High |
| 2020-04-20 | Negative Oil Prices (first time) | Global | High |
| 2022-02-24 | Russia-Ukraine War | Europe | High |
| 2022-10-05 | OPEC+ 2M barrel/day cut | Global | High |
| *+ 8 additional events* | See `data/external/key_events.csv` | | |

---

## Assumptions and Limitations

**Key Assumptions**: Data quality (accurate prices), market efficiency (prices reflect information), event timing (immediate effects), linearity (within regimes), independence (change points), stationarity (within regimes).

**Critical Limitation - Correlation vs. Causation**: Identifying statistical correlation between events and change points **does not prove causation**. Change points may result from identified events, other contemporaneous events, accumulated factors, market anticipation, or random fluctuations. Establishing causation requires controlled experiments (impossible for historical data), counterfactual analysis, and expert validation. **Our Approach**: Identify correlations, quantify impacts probabilistically, present as "likely associations" rather than proven causation.

**Other Limitations**: Model assumptions (single change points, normal returns), data limitations (daily frequency, no volume data), temporal market evolution, unaccounted external factors.

---

## Time Series Analysis: Initial Findings

**Dataset**: ~9,000 daily prices (May 20, 1987 - September 30, 2022). **Trend Analysis**: Overall upward trend with statistically significant positive slope (R² > 0.5, p < 0.05), indicating long-term appreciation despite volatility. **Visualization**: Price time series plot (see `reports/price_series.png`) shows complete series from ~$18/barrel (1987) to >$140/barrel peak (2008) with multiple rapid changes.

**Stationarity**: ADF and KPSS tests confirm **non-stationarity** (p > 0.05), confirming need for change point modeling rather than standard time series methods. Log returns are more stationary but overall series requires structural break detection.

**Volatility Analysis**: Annualized volatility ~30-40% with significant clustering. Volatility spikes correspond to major geopolitical/economic events (2008 Financial Crisis, 2020 COVID-19), supporting hypothesis that events cause structural changes. **Visualization**: Rolling volatility plot (see `reports/volatility_series.png`) demonstrates clustering patterns where spikes align with major crises.

**Results saved to** `reports/` directory (summary_statistics.csv, trend_analysis.csv, stationarity_tests.csv, volatility_analysis.csv).

---

## Change Point Model Understanding

**Purpose**: Identify structural breaks where price dynamics (mean, volatility, trend) shift due to external events. **Bayesian Approach**: Using PyMC with **MCMC sampling** (NUTS algorithm) to estimate posterior distributions of change point locations and parameters, providing credible intervals and uncertainty quantification. **Expected Outputs**: Change point dates with 95% credible intervals, before/after parameter values (mean prices), percentage changes, probability distributions, event associations based on temporal proximity. **Limitations**: Assume abrupt changes (may miss gradual transitions), may detect spurious change points, require careful model specification and convergence checking.

---

## Next Steps: Roadmap

### Task 2: Bayesian Change Point Modeling
**Activities**: (1) Build PyMC model (discrete uniform prior for switch point τ, before/after parameters μ₁, μ₂), (2) Run MCMC sampling with convergence checking (R-hat < 1.01, trace plots), (3) Identify change points (posterior distributions, credible intervals), (4) Quantify impacts (percentage changes, probabilistic statements), (5) Associate with events (temporal proximity analysis). **Connection**: Task 1 analysis informs model specification; event dataset enables association.

### Task 3: Interactive Dashboard
**Activities**: (1) Flask backend (API endpoints: `/api/prices`, `/api/change-points`, `/api/events`), (2) React frontend (interactive visualizations, filters, date selectors, event highlighting), (3) Features (historical trends, event correlations, key indicators, responsive design). **Connection**: Task 1 visualizations inform design; event dataset enables highlighting; analysis results serve as API data sources.

---

## Deliverables

✅ **1-2 Page Analysis Workflow** (This document)  
✅ **Event Data CSV** (`data/external/key_events.csv` - 18 events)  
✅ **Assumptions and Limitations** (Section 3, including correlation vs. causation)  
✅ **Time Series Analysis** (Section 4: trend, stationarity, volatility findings)  
✅ **Visualizations** (6 plots in `reports/` directory: price_series.png, volatility_series.png, price_with_events.png, returns_series.png, and distribution plots)  
✅ **Change Point Model Understanding** (Section 5)  
✅ **Next Steps Roadmap** (Section 6)

**To Generate Results**: Run `python run_task1.py` or execute `notebooks/01_task1_foundation_analysis.py`

---

**Document Version**: 3.2 | **Last Updated**: 2026-02-04 | **Author**: Birhan Energies Data Science Team
