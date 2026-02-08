"""
Data preprocessing module for time series analysis.

This module provides classes for preprocessing Brent oil price data
for statistical analysis, including stationarity testing and
volatility analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import logging
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import acorr_ljungbox

logger = logging.getLogger(__name__)


class PreprocessingError(Exception):
    """Custom exception for preprocessing errors."""
    pass


class TimeSeriesAnalyzer:
    """
    Class for analyzing time series properties of Brent oil prices.
    
    Performs trend analysis, stationarity testing, and volatility analysis.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the analyzer.
        
        Args:
            data: DataFrame with 'Date' and 'Price' columns
        """
        if 'Date' not in data.columns or 'Price' not in data.columns:
            raise PreprocessingError(
                "Data must contain 'Date' and 'Price' columns"
            )
        
        self.data = data.copy()
        self.data = self.data.set_index('Date').sort_index()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
    def analyze_trend(self) -> Dict:
        """
        Analyze trend in the price series.
        
        Returns:
            Dictionary with trend statistics
        """
        try:
            prices = self.data['Price']
            
            # Linear trend
            x = np.arange(len(prices))
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                x, prices.values
            )
            
            # Time-based trend (using actual dates)
            date_numeric = pd.to_numeric(prices.index)
            slope_date, intercept_date, r_date, p_date, std_err_date = (
                stats.linregress(date_numeric, prices.values)
            )
            
            trend_analysis = {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value ** 2,
                'p_value': p_value,
                'trend_direction': 'increasing' if slope > 0 else 'decreasing',
                'slope_per_year': slope_date * 365.25 * 24 * 60 * 60 * 1e9,  # Convert to per year
                'is_significant': p_value < 0.05
            }
            
            self.logger.info(
                f"Trend analysis: {trend_analysis['trend_direction']} "
                f"(R²={trend_analysis['r_squared']:.4f}, p={p_value:.4f})"
            )
            
            return trend_analysis
            
        except Exception as e:
            error_msg = f"Error in trend analysis: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise PreprocessingError(error_msg) from e
    
    def test_stationarity(
        self, 
        method: str = 'adf',
        maxlag: Optional[int] = None
    ) -> Dict:
        """
        Test for stationarity using ADF or KPSS test.
        
        Args:
            method: 'adf' for Augmented Dickey-Fuller, 'kpss' for KPSS
            maxlag: Maximum lag for ADF test
            
        Returns:
            Dictionary with test results
        """
        try:
            prices = self.data['Price'].values
            
            if method == 'adf':
                result = adfuller(prices, maxlag=maxlag, autolag='AIC')
                test_statistic = result[0]
                p_value = result[1]
                critical_values = result[4]
                is_stationary = p_value < 0.05
                
                stationarity_result = {
                    'test': 'ADF',
                    'test_statistic': test_statistic,
                    'p_value': p_value,
                    'critical_values': critical_values,
                    'is_stationary': is_stationary,
                    'interpretation': (
                        'Stationary' if is_stationary 
                        else 'Non-stationary'
                    )
                }
                
            elif method == 'kpss':
                import warnings
                # Suppress the interpolation warning for extreme test statistics
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', category=UserWarning)
                    result = kpss(prices, regression='ct', nlags='auto')
                
                test_statistic = result[0]
                p_value = result[1]
                critical_values = result[3]
                
                # Handle extreme test statistics (outside lookup table range)
                # If p-value is very small, it indicates strong non-stationarity
                if p_value < 0.001:
                    p_value = 0.001  # Set minimum p-value for extreme cases
                    p_value_note = " (approximate - statistic outside lookup table range)"
                else:
                    p_value_note = ""
                
                is_stationary = p_value > 0.05
                
                stationarity_result = {
                    'test': 'KPSS',
                    'test_statistic': test_statistic,
                    'p_value': p_value,
                    'p_value_note': p_value_note,
                    'critical_values': critical_values,
                    'is_stationary': is_stationary,
                    'interpretation': (
                        'Stationary' if is_stationary 
                        else 'Non-stationary'
                    )
                }
            else:
                raise ValueError(f"Unknown method: {method}. Use 'adf' or 'kpss'")
            
            p_note = stationarity_result.get('p_value_note', '')
            self.logger.info(
                f"{method.upper()} test: {stationarity_result['interpretation']} "
                f"(p={p_value:.4f}{p_note})"
            )
            
            return stationarity_result
            
        except Exception as e:
            error_msg = f"Error in stationarity test: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise PreprocessingError(error_msg) from e
    
    def analyze_volatility(self, window: int = 30) -> Dict:
        """
        Analyze volatility patterns in the price series.
        
        Args:
            window: Rolling window size for volatility calculation
            
        Returns:
            Dictionary with volatility statistics
        """
        try:
            prices = self.data['Price']
            
            # Compute log returns
            returns = np.log(prices / prices.shift(1)).dropna()
            
            # Rolling volatility (standard deviation)
            rolling_vol = returns.rolling(window=window).std()
            
            # Overall statistics
            volatility_stats = {
                'mean_volatility': returns.std(),
                'annualized_volatility': returns.std() * np.sqrt(252),  # Assuming trading days
                'min_volatility': rolling_vol.min(),
                'max_volatility': rolling_vol.max(),
                'mean_rolling_volatility': rolling_vol.mean(),
                'volatility_clustering': self._test_volatility_clustering(returns),
                'rolling_volatility': rolling_vol
            }
            
            self.logger.info(
                f"Volatility analysis: Mean={volatility_stats['mean_volatility']:.4f}, "
                f"Annualized={volatility_stats['annualized_volatility']:.2%}"
            )
            
            return volatility_stats
            
        except Exception as e:
            error_msg = f"Error in volatility analysis: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise PreprocessingError(error_msg) from e
    
    def _test_volatility_clustering(self, returns: pd.Series) -> Dict:
        """
        Test for volatility clustering using Ljung-Box test.
        
        Args:
            returns: Series of returns
            
        Returns:
            Dictionary with test results
        """
        try:
            # Test on squared returns (proxy for volatility)
            squared_returns = returns ** 2
            
            # Ljung-Box test
            lb_test = acorr_ljungbox(
                squared_returns, 
                lags=10, 
                return_df=True
            )
            
            p_value = lb_test['lb_pvalue'].iloc[-1]
            
            return {
                'has_clustering': p_value < 0.05,
                'p_value': p_value,
                'interpretation': (
                    'Volatility clustering present' if p_value < 0.05
                    else 'No significant volatility clustering'
                )
            }
            
        except Exception as e:
            self.logger.warning(f"Error in volatility clustering test: {e}")
            return {'has_clustering': None, 'error': str(e)}
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics for the price series.
        
        Returns:
            DataFrame with summary statistics
        """
        try:
            prices = self.data['Price']
            
            stats_dict = {
                'count': len(prices),
                'mean': prices.mean(),
                'std': prices.std(),
                'min': prices.min(),
                '25%': prices.quantile(0.25),
                '50%': prices.quantile(0.50),
                '75%': prices.quantile(0.75),
                'max': prices.max(),
                'skewness': prices.skew(),
                'kurtosis': prices.kurtosis()
            }
            
            return pd.DataFrame([stats_dict])
            
        except Exception as e:
            error_msg = f"Error computing summary statistics: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise PreprocessingError(error_msg) from e
