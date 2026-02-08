"""
Unit tests for data loading module.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_processing.load_data import BrentOilDataLoader, DataLoadError


class TestBrentOilDataLoader(unittest.TestCase):
    """Test cases for BrentOilDataLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data_path = Path(__file__).parent.parent / "data" / "raw" / "BrentOilPrices.csv"
        self.loader = BrentOilDataLoader(self.data_path)
    
    def test_initialization(self):
        """Test loader initialization."""
        self.assertIsNotNone(self.loader)
        self.assertEqual(self.loader.data_path, self.data_path)
        self.assertIsNone(self.loader.data)
    
    def test_load_data(self):
        """Test data loading."""
        df = self.loader.load()
        
        # Check that data is loaded
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        
        # Check required columns
        self.assertIn('Date', df.columns)
        self.assertIn('Price', df.columns)
        
        # Check data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['Date']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['Price']))
        
        # Check no missing values
        self.assertFalse(df['Date'].isna().any())
        self.assertFalse(df['Price'].isna().any())
        
        # Check data is sorted by date
        self.assertTrue(df['Date'].is_monotonic_increasing)
    
    def test_get_data_before_load(self):
        """Test that get_data raises error if data not loaded."""
        with self.assertRaises(DataLoadError):
            self.loader.get_data()
    
    def test_get_data_after_load(self):
        """Test that get_data returns data after loading."""
        self.loader.load()
        data = self.loader.get_data()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)
    
    def test_compute_returns_log(self):
        """Test log returns computation."""
        self.loader.load()
        returns = self.loader.compute_returns(method='log')
        
        self.assertIsInstance(returns, pd.Series)
        self.assertGreater(len(returns), 0)
        self.assertFalse(returns.isna().any())
    
    def test_compute_returns_simple(self):
        """Test simple returns computation."""
        self.loader.load()
        returns = self.loader.compute_returns(method='simple')
        
        self.assertIsInstance(returns, pd.Series)
        self.assertGreater(len(returns), 0)
        self.assertFalse(returns.isna().any())
    
    def test_compute_returns_invalid_method(self):
        """Test that invalid method raises error."""
        self.loader.load()
        with self.assertRaises(ValueError):
            self.loader.compute_returns(method='invalid')
    
    def test_nonexistent_file(self):
        """Test that nonexistent file raises error."""
        loader = BrentOilDataLoader(Path("nonexistent.csv"))
        with self.assertRaises(DataLoadError):
            loader.load()


if __name__ == '__main__':
    unittest.main()
