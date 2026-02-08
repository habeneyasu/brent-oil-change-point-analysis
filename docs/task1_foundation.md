# Task 1: Laying the Foundation for Analysis

## Executive Summary

This document outlines the foundational analysis for detecting change points in Brent oil price time series data and associating them with major geopolitical and economic events. The analysis employs Bayesian change point detection methods using PyMC to identify structural breaks and quantify their impact on oil prices.

---

## 1. Data Analysis Workflow

### 1.1 Analysis Steps

Our analysis follows a systematic workflow from data ingestion to insight generation:

1. **Data Loading and Validation**
   - Load Brent oil price data (May 20, 1987 - September 30, 2022)
   - Handle multiple date formats (DD-MMM-YY and MMM DD, YYYY)
   - Validate data quality (missing values, outliers, date consistency)
   - Convert prices to numeric format

2. **Data Preprocessing**
   - Parse and standardize date formats
   - Compute log returns: `r_t = log(P_t / P_{t-1})`
   - Handle missing values and data gaps
   - Create time-indexed series for analysis

3. **Exploratory Data Analysis (EDA)**
   - Visualize price series over time
   - Analyze trend components (linear and non-linear)
   - Test for stationarity (ADF and KPSS tests)
   - Examine volatility patterns and clustering
   - Compute summary statistics and distributions

4. **Event Data Compilation**
   - Research and compile major geopolitical events
   - Document OPEC decisions and production changes
   - Identify economic shocks and crises
   - Create structured event dataset with dates and descriptions

5. **Bayesian Change Point Modeling**
   - Define change point model with PyMC
   - Specify prior distributions for parameters
   - Run MCMC sampling (NUTS algorithm)
   - Assess convergence (R-hat, trace plots)
   - Extract posterior distributions

6. **Change Point Detection and Analysis**
   - Identify most probable change point dates
   - Quantify parameter changes (mean, volatility)
   - Calculate credible intervals
   - Associate change points with events

7. **Impact Quantification**
   - Compute price changes before/after change points
   - Calculate percentage changes and statistical significance
   - Estimate economic impact in USD terms
   - Create visualizations linking events to price changes

8. **Insight Generation and Reporting**
   - Synthesize findings into actionable insights
   - Create interactive dashboard
   - Generate comprehensive report
   - Document assumptions and limitations

### 1.2 Key Processes

- **Statistical Testing**: ADF and KPSS tests for stationarity
- **Volatility Analysis**: Rolling window standard deviation, GARCH-like patterns
- **Bayesian Inference**: MCMC sampling with PyMC for parameter estimation
- **Model Comparison**: Multiple change point models (single vs. multiple change points)
- **Visualization**: Time series plots, posterior distributions, event overlays

---

## 2. Event Data Compilation

We have compiled a structured dataset of **18 key events** affecting Brent oil prices from 1990 to 2022. The events are categorized by:

- **Event Type**: Geopolitical conflicts, OPEC decisions, economic crises, natural disasters
- **Region**: Middle East, Global, Asia, Europe, North America
- **Impact Level**: High, Medium (based on historical significance)

Key events include:
- Gulf War (1990-1991)
- Asian Financial Crisis (1998)
- 9/11 Attacks (2001)
- Iraq War (2003)
- Global Financial Crisis (2008)
- Arab Spring (2011)
- OPEC Production Decisions (2014, 2022)
- COVID-19 Pandemic (2020)
- Russia-Ukraine War (2022)

The complete event dataset is stored in `data/external/key_events.csv` with columns:
- `Event_Date`: Date of event (YYYY-MM-DD)
- `Event_Type`: Category of event
- `Event_Description`: Detailed description
- `Region`: Geographic region affected
- `Impact_Level`: Expected impact magnitude

---

## 3. Assumptions and Limitations

### 3.1 Key Assumptions

1. **Data Quality**: We assume the provided price data is accurate and representative of actual market prices. Minor data quality issues (missing values, outliers) are handled through robust preprocessing.

2. **Market Efficiency**: We assume the oil market is generally efficient, meaning prices reflect available information. However, we acknowledge short-term inefficiencies and market overreactions.

3. **Event Timing**: We assume events have immediate or near-immediate effects on prices. In reality, some events may have delayed effects or anticipatory price movements.

4. **Linearity**: Our initial models assume linear relationships. Non-linear effects and regime changes are addressed through change point detection.

5. **Independence**: We assume that change points are independent events, though in reality, events may be correlated or have cascading effects.

6. **Stationarity**: For certain analyses, we assume stationarity within regimes (between change points), though the overall series is non-stationary.

### 3.2 Limitations

1. **Correlation vs. Causation**: 
   - **Critical Limitation**: Identifying a statistical correlation between an event date and a change point does **not** prove causation.
   - Change points may be caused by:
     - The specific event we identify
     - Other contemporaneous events
     - Accumulated effects of multiple factors
     - Market anticipation of future events
     - Random market fluctuations
   - To establish causation, we would need:
     - Controlled experiments (impossible for historical data)
     - Counterfactual analysis
     - Detailed market microstructure data
     - Expert domain knowledge validation

2. **Model Limitations**:
   - Single change point models may miss multiple simultaneous changes
   - Assumes normal distribution of returns (may not hold during crises)
   - Does not account for time-varying volatility explicitly
   - May not capture gradual transitions (assumes abrupt changes)

3. **Data Limitations**:
   - Daily data may miss intraday volatility
   - No volume or trading data
   - Limited to Brent prices (may not reflect all market dynamics)
   - Historical data may have reporting errors or gaps

4. **Temporal Limitations**:
   - Analysis covers 1987-2022, but market structure has evolved
   - Early period may have different dynamics than recent period
   - Structural breaks in market mechanisms not captured

5. **External Factors**:
   - Cannot account for all external factors (weather, technology, regulations)
   - OPEC decisions may be influenced by factors not in our dataset
   - Currency fluctuations and exchange rate effects not directly modeled

### 3.3 Statistical Correlation vs. Causal Impact

**Statistical Correlation**:
- We can identify that a change point occurs near an event date
- We can quantify the magnitude of price changes
- We can calculate probabilities and confidence intervals
- We can test statistical significance

**Causal Impact** (Requires Additional Evidence):
- Requires establishing a causal mechanism
- Needs to rule out alternative explanations
- May require instrumental variables or natural experiments
- Benefits from domain expertise and qualitative analysis

**Our Approach**:
- We identify correlations and associations
- We quantify impacts probabilistically
- We acknowledge limitations in causal inference
- We present findings as "likely associations" rather than proven causation
- We recommend further analysis for policy decisions

---

## 4. Communication Channels

### 4.1 Primary Channels

1. **Interactive Dashboard** (React + Flask)
   - Target: Investors, analysts, policymakers
   - Features: Interactive visualizations, event filtering, date range selection
   - Access: Web-based, responsive design

2. **Comprehensive Report** (PDF/Markdown)
   - Target: Government bodies, executive decision-makers
   - Content: Executive summary, methodology, findings, recommendations
   - Format: Professional, citation-ready

3. **Jupyter Notebooks**
   - Target: Data scientists, researchers, technical stakeholders
   - Content: Reproducible analysis, code, visualizations
   - Format: Interactive, educational

4. **Presentation Slides**
   - Target: Stakeholder meetings, conferences
   - Content: Key findings, visualizations, actionable insights
   - Format: PowerPoint/PDF, concise

### 4.2 Communication Formats

- **Visualizations**: Time series plots, posterior distributions, event overlays
- **Tables**: Summary statistics, change point results, impact quantification
- **Narratives**: Written explanations, interpretations, recommendations
- **Code**: Reproducible Python scripts and notebooks

### 4.3 Stakeholder-Specific Communication

- **Investors**: Focus on risk management, price forecasting, volatility patterns
- **Policymakers**: Emphasis on economic stability, energy security, policy implications
- **Energy Companies**: Operational planning, supply chain management, cost control
- **Researchers**: Methodology, statistical rigor, reproducibility

---

## 5. Key References and Concepts

### 5.1 Bayesian Change Point Detection

**Core Concept**: Identify points in time where the underlying data-generating process changes. In our context, this means detecting when oil price dynamics (mean, volatility, trend) shift.

**Key References**:
- Barry, D., & Hartigan, J. A. (1993). A Bayesian analysis for change point problems. *Journal of the American Statistical Association*.
- Adams, R. P., & MacKay, D. J. (2007). Bayesian online changepoint detection. *arXiv preprint*.

**PyMC Implementation**:
- Uses probabilistic programming for Bayesian inference
- MCMC sampling (NUTS algorithm) for posterior estimation
- Allows uncertainty quantification through posterior distributions

### 5.2 Time Series Properties

**Trend**: Long-term direction of prices (increasing, decreasing, or stable)
- **Analysis Method**: Linear regression, moving averages
- **Implication**: Non-stationary series requires differencing or change point modeling

**Stationarity**: Statistical properties (mean, variance) constant over time
- **Tests**: Augmented Dickey-Fuller (ADF), KPSS
- **Implication**: Stationary series easier to model; non-stationary requires special treatment

**Volatility**: Measure of price variability
- **Patterns**: Volatility clustering (high volatility followed by high volatility)
- **Implication**: May require GARCH models or regime-switching models

### 5.3 Change Point Models

**Purpose**: 
- Identify structural breaks in time series
- Detect regime changes (calm vs. volatile periods)
- Quantify impact of events on price dynamics
- Support causal inference (when combined with event data)

**How They Help**:
- Objectively identify when prices shift
- Provide uncertainty estimates (credible intervals)
- Allow probabilistic statements about change magnitudes
- Enable association with external events

**Limitations**:
- Assume abrupt changes (may miss gradual transitions)
- May detect spurious change points
- Require careful model specification
- Results depend on prior assumptions

---

## 6. Time Series Properties Analysis

### 6.1 Expected Properties

Based on preliminary analysis of Brent oil prices:

**Trend**:
- Overall upward trend from 1987 to 2022
- Multiple periods of rapid increase and decrease
- Long-term average price increase

**Stationarity**:
- **Expected**: Non-stationary (prices have trend and varying volatility)
- **Log Returns**: Should be more stationary than prices
- **Implication**: Change point models should work on prices or returns

**Volatility**:
- **Pattern**: Volatility clustering (periods of high/low volatility)
- **Crises**: Increased volatility during economic/political crises
- **Implication**: May need to model volatility changes separately

### 6.2 Modeling Choices Informed by Properties

1. **Use Log Returns**: More stationary, better for statistical modeling
2. **Change Point on Prices**: Directly interpretable in USD terms
3. **Multiple Change Points**: Account for multiple regime changes
4. **Volatility Modeling**: Separate change points for mean and volatility
5. **Bayesian Approach**: Quantify uncertainty in change point locations

---

## 7. Expected Outputs of Change Point Analysis

### 7.1 Primary Outputs

1. **Change Point Dates**:
   - Most probable change point dates (posterior mode)
   - Credible intervals (e.g., 95% HPD interval)
   - Probability distribution over possible change points

2. **Parameter Values**:
   - Mean price before change point (μ₁)
   - Mean price after change point (μ₂)
   - Volatility before/after (if modeled)
   - Percentage change: `(μ₂ - μ₁) / μ₁ × 100%`

3. **Uncertainty Quantification**:
   - Posterior distributions for all parameters
   - Credible intervals
   - Probability that change occurred at specific date

4. **Event Associations**:
   - List of events near detected change points
   - Temporal proximity analysis
   - Impact quantification for each event

### 7.2 Limitations of Outputs

1. **Temporal Resolution**: Daily data limits precision to day-level
2. **Model Assumptions**: Results depend on model specification
3. **Multiple Explanations**: Change points may have multiple causes
4. **Anticipation Effects**: Prices may change before events (market anticipation)
5. **Gradual Changes**: May miss gradual transitions if model assumes abrupt changes

### 7.3 Interpretation Guidelines

- **High Probability Change Points**: Strong evidence of structural break
- **Wide Credible Intervals**: High uncertainty about exact timing
- **Large Parameter Changes**: Significant economic impact
- **Event Proximity**: Suggests (but doesn't prove) causal relationship

---

## 8. Deliverables Summary

1. ✅ **Analysis Workflow Document** (This document, Section 1)
2. ✅ **Event Data CSV** (`data/external/key_events.csv` - 18 events)
3. ✅ **Assumptions and Limitations** (Section 3)
4. ✅ **Communication Channels** (Section 4)
5. ✅ **Key References** (Section 5)
6. ✅ **Time Series Properties Analysis** (Section 6)
7. ✅ **Change Point Model Explanation** (Section 5.3)
8. ✅ **Expected Outputs** (Section 7)

---

## 9. Next Steps (Task 2)

1. Implement Bayesian change point model in PyMC
2. Run MCMC sampling and assess convergence
3. Extract and visualize posterior distributions
4. Identify change points and quantify impacts
5. Associate change points with events
6. Generate comprehensive analysis report

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-04  
**Author**: Birhan Energies Data Science Team
