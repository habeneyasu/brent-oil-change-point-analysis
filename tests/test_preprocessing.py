"""
Unit tests for preprocessing module.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_processing.preprocess import TimeSeriesAnalyzer, PreprocessingError


class TestTimeSeriesAnalyzer(unittest.TestCase):
    """Test cases for TimeSeriesAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create sample data
        dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
        prices = 50 + np.cumsum(np.random.randn(100) * 0.5)
        
        self.test_data = pd.DataFrame({
            'Date': dates,
            'Price': prices
        })
        
        self.analyzer = TimeSeriesAnalyzer(self.test_data)
    
    def test_initialization(self):
        """Test analyzer initialization."""
        self.assertIsNotNone(self.analyzer)
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(len(self.analyzer.data), 100)
    
    def test_initialization_missing_columns(self):
        """Test that missing columns raise error."""
        bad_data = pd.DataFrame({'Date': [1, 2, 3]})
        with self.assertRaises(PreprocessingError):
            TimeSeriesAnalyzer(bad_data)
    
    def test_analyze_trend(self):
        """Test trend analysis."""
        result = self.analyzer.analyze_trend()
        
        self.assertIsInstance(result, dict)
        self.assertIn('slope', result)
        self.assertIn('r_squared', result)
        self.assertIn('p_value', result)
        self.assertIn('trend_direction', result)
        self.assertIn('is_significant', result)
    
    def test_test_stationarity_adf(self):
        """Test ADF stationarity test."""
        result = self.analyzer.test_stationarity(method='adf')
        
        self.assertIsInstance(result, dict)
        self.assertIn('test', result)
        self.assertIn('test_statistic', result)
        self.assertIn('p_value', result)
        self.assertIn('is_stationary', result)
        self.assertEqual(result['test'], 'ADF')
    
    def test_test_stationarity_kpss(self):
        """Test KPSS stationarity test."""
        result = self.analyzer.test_stationarity(method='kpss')
        
        self.assertIsInstance(result, dict)
        self.assertIn('test', result)
        self.assertIn('test_statistic', result)
        self.assertIn('p_value', result)
        self.assertIn('is_stationary', result)
        self.assertEqual(result['test'], 'KPSS')
    
    def test_test_stationarity_invalid_method(self):
        """Test that invalid method raises error."""
        with self.assertRaises(ValueError):
            self.analyzer.test_stationarity(method='invalid')
    
    def test_analyze_volatility(self):
        """Test volatility analysis."""
        result = self.analyzer.analyze_volatility(window=30)
        
        self.assertIsInstance(result, dict)
        self.assertIn('mean_volatility', result)
        self.assertIn('annualized_volatility', result)
        self.assertIn('rolling_volatility', result)
        self.assertIsInstance(result['rolling_volatility'], pd.Series)
    
    def test_get_summary_statistics(self):
        """Test summary statistics."""
        stats = self.analyzer.get_summary_statistics()
        
        self.assertIsInstance(stats, pd.DataFrame)
        self.assertGreater(len(stats), 0)
        self.assertIn('mean', stats.columns)
        self.assertIn('std', stats.columns)
        self.assertIn('min', stats.columns)
        self.assertIn('max', stats.columns)


if __name__ == '__main__':
    unittest.main()
