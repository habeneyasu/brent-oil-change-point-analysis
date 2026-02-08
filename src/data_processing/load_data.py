"""
Data loading module for Brent oil price dataset.

This module provides classes and functions for loading and initial processing
of the Brent oil price time series data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """Custom exception for data loading errors."""
    pass


class BrentOilDataLoader:
    """
    Class for loading and initial processing of Brent oil price data.
    
    Handles multiple date formats and provides robust error handling
    for data quality issues.
    """
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the CSV file. If None, uses default path.
        """
        if data_path is None:
            # Default to data/raw directory
            project_root = Path(__file__).parent.parent.parent
            data_path = project_root / "data" / "raw" / "BrentOilPrices.csv"
        
        self.data_path = Path(data_path)
        self.data: Optional[pd.DataFrame] = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
    def load(self) -> pd.DataFrame:
        """
        Load the Brent oil price data from CSV.
        
        Returns:
            DataFrame with Date and Price columns
            
        Raises:
            DataLoadError: If file cannot be loaded or processed
        """
        try:
            if not self.data_path.exists():
                raise DataLoadError(f"Data file not found: {self.data_path}")
            
            self.logger.info(f"Loading data from {self.data_path}")
            
            # Read CSV
            df = pd.read_csv(self.data_path)
            
            # Validate columns
            required_columns = ['Date', 'Price']
            if not all(col in df.columns for col in required_columns):
                raise DataLoadError(
                    f"Missing required columns. Expected {required_columns}, "
                    f"got {list(df.columns)}"
                )
            
            # Parse dates - handle multiple formats
            df['Date'] = self._parse_dates(df['Date'])
            
            # Convert Price to numeric, handling any string values
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            
            # Remove rows with missing values
            initial_rows = len(df)
            df = df.dropna()
            removed_rows = initial_rows - len(df)
            
            if removed_rows > 0:
                self.logger.warning(
                    f"Removed {removed_rows} rows with missing values"
                )
            
            # Sort by date
            df = df.sort_values('Date').reset_index(drop=True)
            
            # Validate data quality
            self._validate_data(df)
            
            self.data = df
            self.logger.info(
                f"Successfully loaded {len(df)} records from "
                f"{df['Date'].min()} to {df['Date'].max()}"
            )
            
            return df
            
        except FileNotFoundError as e:
            error_msg = f"File not found: {self.data_path}"
            self.logger.error(error_msg)
            raise DataLoadError(error_msg) from e
        except pd.errors.EmptyDataError as e:
            error_msg = f"Data file is empty: {self.data_path}"
            self.logger.error(error_msg)
            raise DataLoadError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error loading data: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise DataLoadError(error_msg) from e
    
    def _parse_dates(self, date_series: pd.Series) -> pd.Series:
        """
        Parse dates handling multiple formats.
        
        Args:
            date_series: Series of date strings
            
        Returns:
            Series of datetime objects
        """
        parsed_dates = []
        
        for date_str in date_series:
            try:
                # Try format: "DD-MMM-YY" (e.g., "20-May-87")
                if isinstance(date_str, str) and '-' in date_str and len(date_str.split('-')) == 3:
                    parsed = pd.to_datetime(date_str, format='%d-%b-%y')
                # Try format: "MMM DD, YYYY" (e.g., "Oct 27, 2022")
                elif isinstance(date_str, str) and ',' in date_str:
                    parsed = pd.to_datetime(date_str, format='%b %d, %Y')
                else:
                    # Try pandas automatic parsing
                    parsed = pd.to_datetime(date_str)
                parsed_dates.append(parsed)
            except Exception as e:
                self.logger.warning(f"Could not parse date '{date_str}': {e}")
                parsed_dates.append(pd.NaT)
        
        return pd.Series(parsed_dates)
    
    def _validate_data(self, df: pd.DataFrame) -> None:
        """
        Validate data quality.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            DataLoadError: If data quality issues are found
        """
        # Check for negative prices
        negative_prices = (df['Price'] < 0).sum()
        if negative_prices > 0:
            self.logger.warning(f"Found {negative_prices} negative prices")
        
        # Check for unrealistic prices (e.g., > $200)
        unrealistic_prices = (df['Price'] > 200).sum()
        if unrealistic_prices > 0:
            self.logger.warning(
                f"Found {unrealistic_prices} prices above $200/barrel"
            )
        
        # Check for duplicate dates
        duplicate_dates = df['Date'].duplicated().sum()
        if duplicate_dates > 0:
            self.logger.warning(f"Found {duplicate_dates} duplicate dates")
        
        # Check date range
        date_range = (df['Date'].max() - df['Date'].min()).days
        if date_range < 365:
            self.logger.warning(
                f"Data covers only {date_range} days, expected longer period"
            )
    
    def get_data(self) -> pd.DataFrame:
        """
        Get the loaded data.
        
        Returns:
            DataFrame with loaded data
            
        Raises:
            DataLoadError: If data has not been loaded yet
        """
        if self.data is None:
            raise DataLoadError("Data has not been loaded. Call load() first.")
        return self.data.copy()
    
    def compute_returns(self, method: str = 'log') -> pd.Series:
        """
        Compute returns from prices.
        
        Args:
            method: 'log' for log returns, 'simple' for simple returns
            
        Returns:
            Series of returns
        """
        if self.data is None:
            raise DataLoadError("Data has not been loaded. Call load() first.")
        
        prices = self.data['Price']
        
        if method == 'log':
            returns = np.log(prices / prices.shift(1))
        elif method == 'simple':
            returns = (prices / prices.shift(1)) - 1
        else:
            raise ValueError(f"Unknown method: {method}. Use 'log' or 'simple'")
        
        # Remove first NaN value
        returns = returns.dropna()
        
        self.logger.info(f"Computed {method} returns: {len(returns)} values")
        
        return returns
