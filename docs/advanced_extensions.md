# Advanced Extensions and Future Work

This document outlines advanced modeling approaches and extensions that could enhance the Brent oil price change point analysis beyond the current Bayesian single change point model.

## 1. Exploring Other Potential Factors

### 1.1 Additional Data Sources

To build a more comprehensive explanatory model, we could incorporate the following data sources:

#### Macroeconomic Variables
- **GDP Growth Rates**: Economic growth affects oil demand
  - Source: World Bank, IMF, national statistics offices
  - Frequency: Quarterly or annual
  - Impact: Higher GDP growth → increased oil demand → higher prices

- **Inflation Rates**: Affects purchasing power and real oil prices
  - Source: Central banks, statistical offices
  - Frequency: Monthly
  - Impact: High inflation → reduced real purchasing power → demand effects

- **Exchange Rates**: Currency fluctuations affect oil prices (USD-denominated)
  - Source: Central banks, financial data providers
  - Frequency: Daily
  - Impact: Stronger USD → higher oil prices for non-USD countries → demand effects

#### Market-Specific Variables
- **Oil Inventories**: Stock levels indicate supply/demand balance
  - Source: EIA (US), IEA (International)
  - Frequency: Weekly
  - Impact: High inventories → downward price pressure

- **Production Levels**: OPEC and non-OPEC production data
  - Source: OPEC, EIA, IEA
  - Frequency: Monthly
  - Impact: Production cuts → supply reduction → price increase

- **Refining Capacity Utilization**: Indicates downstream demand
  - Source: EIA, industry reports
  - Frequency: Weekly/Monthly
  - Impact: High utilization → strong demand → price support

#### Financial Market Variables
- **Stock Market Indices**: Economic sentiment indicator
  - Source: Financial data providers (Yahoo Finance, Bloomberg)
  - Frequency: Daily
  - Impact: Market sentiment → risk appetite → commodity demand

- **Currency Strength Index**: USD index (DXY)
  - Source: Federal Reserve, financial data providers
  - Frequency: Daily
  - Impact: Strong USD → lower oil prices (inverse relationship)

### 1.2 Data Integration Approach

```python
# Conceptual framework for multi-factor model
class MultiFactorChangePointModel:
    """
    Extended change point model incorporating multiple factors.
    """
    
    def __init__(self, oil_prices, gdp, inflation, exchange_rates, 
                 inventories, production):
        self.oil_prices = oil_prices
        self.gdp = gdp
        self.inflation = inflation
        self.exchange_rates = exchange_rates
        self.inventories = inventories
        self.production = production
    
    def build_model(self):
        """
        Build Bayesian change point model with multiple factors.
        
        Model structure:
        - Change point in oil price dynamics
        - Simultaneous changes in:
          * Oil price mean and volatility
          * Relationship with macroeconomic factors
          * Factor loadings (how much each factor affects prices)
        """
        with pm.Model() as model:
            # Change point location
            tau = pm.DiscreteUniform("tau", lower=1, upper=n_obs-1)
            
            # Oil price parameters (before/after)
            mu1_oil = pm.Normal("mu1_oil", ...)
            mu2_oil = pm.Normal("mu2_oil", ...)
            
            # Factor loadings (before/after)
            beta_gdp_1 = pm.Normal("beta_gdp_1", ...)  # GDP impact before
            beta_gdp_2 = pm.Normal("beta_gdp_2", ...)  # GDP impact after
            
            beta_inflation_1 = pm.Normal("beta_inflation_1", ...)
            beta_inflation_2 = pm.Normal("beta_inflation_2", ...)
            
            # ... similar for other factors
            
            # Combined mean
            mu_combined = pm.math.switch(
                tau >= time_indices,
                mu1_oil + beta_gdp_1 * gdp + beta_inflation_1 * inflation + ...,
                mu2_oil + beta_gdp_2 * gdp + beta_inflation_2 * inflation + ...
            )
            
            # Likelihood
            likelihood = pm.Normal("likelihood", mu=mu_combined, ...)
        
        return model
```

### 1.3 Benefits of Multi-Factor Approach

1. **Causal Inference**: Better understanding of which factors drive price changes
2. **Forecasting**: Improved predictions by incorporating leading indicators
3. **Policy Analysis**: Quantify impact of macroeconomic policies on oil prices
4. **Risk Management**: Identify which factors pose greatest risk

### 1.4 Implementation Challenges

- **Data Alignment**: Different frequencies (daily, monthly, quarterly)
- **Missing Data**: Handle gaps in macroeconomic data
- **Model Complexity**: More parameters → longer MCMC sampling
- **Interpretability**: Balance between complexity and understanding

---

## 2. Advanced Models

### 2.1 Vector Autoregression (VAR) Models

#### Overview
VAR models analyze dynamic relationships between multiple time series variables simultaneously, capturing feedback effects and lagged relationships.

#### Application to Oil Prices

```python
# Conceptual VAR model structure
from statsmodels.tsa.vector_ar.var_model import VAR

class OilPriceVARModel:
    """
    VAR model for oil prices and macroeconomic variables.
    """
    
    def __init__(self, data):
        """
        Data should contain:
        - Oil prices
        - GDP growth
        - Exchange rates
        - Inflation
        - Other relevant variables
        """
        self.data = data
    
    def build_model(self, lags=4):
        """
        Build VAR model with specified lag order.
        
        Model: Y_t = A_1 * Y_{t-1} + A_2 * Y_{t-2} + ... + A_p * Y_{t-p} + e_t
        
        Where Y_t is a vector of [oil_price, gdp, exchange_rate, ...]
        """
        model = VAR(self.data)
        var_model = model.fit(lags)
        return var_model
    
    def analyze_impulse_response(self):
        """
        Analyze how shocks to one variable affect others.
        
        Example: What happens to oil prices if GDP increases by 1%?
        """
        irf = self.model.irf(periods=20)
        return irf
    
    def forecast(self, steps=10):
        """
        Forecast future values of all variables.
        """
        forecast = self.model.forecast(self.data.values[-self.lags:], steps)
        return forecast
```

#### Advantages
- **Dynamic Relationships**: Captures how variables influence each other over time
- **Feedback Effects**: Models bidirectional causality
- **Forecasting**: Can forecast multiple variables simultaneously
- **Impulse Response**: Understand how shocks propagate through the system

#### Limitations
- **Stationarity Required**: All variables must be stationary
- **Lag Selection**: Need to determine optimal number of lags
- **Curse of Dimensionality**: Many variables → many parameters
- **No Structural Breaks**: Standard VAR doesn't handle change points

#### Extensions
- **Structural VAR (SVAR)**: Impose economic theory restrictions
- **Bayesian VAR (BVAR)**: Incorporate prior information
- **VAR with Change Points**: Combine VAR with change point detection

### 2.2 Markov-Switching Models

#### Overview
Markov-Switching models explicitly define different "regimes" or states (e.g., calm vs. volatile markets) and allow the model parameters to switch between these regimes.

#### Application to Oil Prices

```python
# Conceptual Markov-Switching model
import pymc as pm

class MarkovSwitchingOilPriceModel:
    """
    Markov-Switching model for oil prices with regime changes.
    """
    
    def build_model(self, n_regimes=2):
        """
        Build Markov-Switching model.
        
        Regimes:
        - Regime 1: "Calm" - low volatility, stable prices
        - Regime 2: "Volatile" - high volatility, price swings
        
        Model switches between regimes based on transition probabilities.
        """
        with pm.Model() as model:
            # Transition probabilities
            # P(regime_t = j | regime_{t-1} = i)
            p_11 = pm.Beta("p_11", alpha=2, beta=2)  # Stay in calm
            p_12 = 1 - p_11  # Switch to volatile
            p_22 = pm.Beta("p_22", alpha=2, beta=2)  # Stay in volatile
            p_21 = 1 - p_22  # Switch to calm
            
            transition_matrix = pm.math.stack([
                [p_11, p_12],
                [p_21, p_22]
            ])
            
            # Regime-specific parameters
            mu_calm = pm.Normal("mu_calm", mu=50, sigma=10)
            mu_volatile = pm.Normal("mu_volatile", mu=50, sigma=10)
            sigma_calm = pm.HalfNormal("sigma_calm", sigma=5)
            sigma_volatile = pm.HalfNormal("sigma_volatile", sigma=20)
            
            # Hidden Markov chain for regimes
            # (This is simplified - full implementation requires
            #  more complex state space modeling)
            
            # Likelihood depends on current regime
            # ...
        
        return model
```

#### Advantages
- **Explicit Regimes**: Clearly identifies market states
- **Smooth Transitions**: Models gradual regime changes
- **Interpretability**: Easy to understand "calm" vs "volatile" periods
- **Forecasting**: Can predict future regime probabilities

#### Limitations
- **Computational Complexity**: More complex than simple change point models
- **Regime Identification**: Need to determine number of regimes
- **Parameter Estimation**: More parameters to estimate
- **Data Requirements**: Need sufficient data in each regime

#### Extensions
- **Time-Varying Transition Probabilities**: Allow transition probabilities to change over time
- **Multiple Regimes**: More than 2 regimes (e.g., calm, moderate, volatile)
- **Regime-Dependent Volatility**: Different volatility in each regime

### 2.3 Model Comparison Framework

```python
class ModelComparison:
    """
    Framework for comparing different models.
    """
    
    def compare_models(self, models_dict):
        """
        Compare multiple models using information criteria.
        
        Models to compare:
        - Simple change point model (current)
        - Multi-factor change point model
        - VAR model
        - Markov-Switching model
        """
        results = {}
        
        for name, model in models_dict.items():
            # Fit model
            trace = model.sample()
            
            # Calculate information criteria
            loo = az.loo(trace)  # Leave-One-Out cross-validation
            waic = az.waic(trace)  # Widely Applicable Information Criterion
            
            results[name] = {
                'loo': loo,
                'waic': waic,
                'trace': trace
            }
        
        # Compare models
        comparison = az.compare(results)
        return comparison
```

---

## 3. Implementation Roadmap

### Phase 1: Data Collection and Integration
1. Identify data sources for GDP, inflation, exchange rates
2. Develop data collection pipeline
3. Align data frequencies (interpolation/aggregation)
4. Handle missing data

### Phase 2: Multi-Factor Model Development
1. Extend Bayesian change point model to include factors
2. Implement factor loading estimation
3. Test model convergence and diagnostics
4. Validate against simple model

### Phase 3: VAR Model Implementation
1. Prepare stationary time series
2. Determine optimal lag order
3. Estimate VAR model
4. Analyze impulse responses and forecasts

### Phase 4: Markov-Switching Model
1. Implement regime-switching framework
2. Estimate transition probabilities
3. Identify regime periods
4. Compare with change point model

### Phase 5: Model Comparison and Selection
1. Implement model comparison framework
2. Use information criteria (LOO, WAIC)
3. Cross-validation
4. Select best model(s) for different use cases

---

## 4. Expected Insights from Advanced Models

### Multi-Factor Model
- Which macroeconomic factors have strongest impact on oil prices?
- How do factor relationships change at change points?
- Can we predict price changes from leading indicators?

### VAR Model
- What are the dynamic relationships between oil prices and macro variables?
- How do shocks propagate through the system?
- What are the forecast horizons for different variables?

### Markov-Switching Model
- What are the characteristics of different market regimes?
- How long do regimes typically last?
- What triggers regime switches?

---

## 5. Conclusion

These advanced extensions would provide:
1. **Deeper Understanding**: Causal relationships and mechanisms
2. **Better Forecasting**: Multi-variable predictions
3. **Regime Identification**: Explicit market state recognition
4. **Policy Insights**: Impact of macroeconomic policies

However, they also require:
- More data collection and preprocessing
- Increased computational resources
- More complex model interpretation
- Longer development time

The current single change point model provides a solid foundation, and these extensions can be implemented incrementally based on specific analytical needs and available resources.
