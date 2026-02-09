"""
Data service module for loading and serving analysis results.

This module provides functions to load data from analysis results
and serve them through the API.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional, List
import logging
import sys

# Add project root to path to import src modules
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from data_processing.load_data import BrentOilDataLoader
from models.event_association import EventAssociator

logger = logging.getLogger(__name__)


class DataServiceError(Exception):
    """Custom exception for data service errors."""
    pass


class DataService:
    """
    Service class for loading and serving analysis data.
    """
    
    def __init__(self):
        """Initialize the data service."""
        self.project_root = project_root
        self.data_dir = project_root / "data"
        self.reports_dir = project_root / "reports"
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Cache for loaded data
        self._price_data_cache: Optional[pd.DataFrame] = None
        self._events_cache: Optional[pd.DataFrame] = None
        self._change_points_cache: Optional[Dict] = None
    
    def get_historical_prices(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Get historical price data.
        
        Args:
            start_date: Start date filter (YYYY-MM-DD format)
            end_date: End date filter (YYYY-MM-DD format)
            
        Returns:
            Dictionary with price data
        """
        try:
            # Load data if not cached
            if self._price_data_cache is None:
                self.logger.info("Loading historical price data...")
                loader = BrentOilDataLoader()
                data = loader.load()
                data['Date'] = pd.to_datetime(data['Date'])
                self._price_data_cache = data
            
            data = self._price_data_cache.copy()
            
            # Apply date filters
            if start_date:
                data = data[data['Date'] >= pd.to_datetime(start_date)]
            if end_date:
                data = data[data['Date'] <= pd.to_datetime(end_date)]
            
            # Convert to JSON-serializable format
            result = {
                'data': data.to_dict('records'),
                'count': len(data),
                'date_range': {
                    'start': data['Date'].min().isoformat() if len(data) > 0 else None,
                    'end': data['Date'].max().isoformat() if len(data) > 0 else None
                },
                'price_range': {
                    'min': float(data['Price'].min()) if len(data) > 0 else None,
                    'max': float(data['Price'].max()) if len(data) > 0 else None,
                    'mean': float(data['Price'].mean()) if len(data) > 0 else None
                }
            }
            
            # Convert dates to strings for JSON
            for record in result['data']:
                if isinstance(record['Date'], pd.Timestamp):
                    record['Date'] = record['Date'].isoformat()
            
            self.logger.info(f"Returned {len(data)} price records")
            return result
            
        except Exception as e:
            error_msg = f"Error loading historical prices: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise DataServiceError(error_msg) from e
    
    def get_change_points(self) -> Dict:
        """
        Get change point results from analysis.
        
        Returns:
            Dictionary with change point data
        """
        try:
            # Try to load from CSV if exists
            cp_file = self.reports_dir / "change_point_association.csv"
            
            if cp_file.exists():
                self.logger.info("Loading change point data from CSV...")
                cp_data = pd.read_csv(cp_file)
                
                # Convert to dict
                if len(cp_data) > 0:
                    result = cp_data.iloc[0].to_dict()
                    
                    # Convert dates
                    for key, value in result.items():
                        if 'date' in key.lower() and pd.notna(value):
                            try:
                                result[key] = pd.to_datetime(value).isoformat()
                            except:
                                pass
                        elif pd.isna(value):
                            result[key] = None
                        elif isinstance(value, (np.integer, np.floating)):
                            result[key] = float(value)
                    
                    return {
                        'change_points': [result],
                        'count': 1
                    }
            
            # If CSV doesn't exist, return empty
            self.logger.warning("Change point data not found, returning empty result")
            return {
                'change_points': [],
                'count': 0,
                'message': 'Change point analysis not yet run. Run Task 2 analysis first.'
            }
            
        except Exception as e:
            error_msg = f"Error loading change points: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise DataServiceError(error_msg) from e
    
    def get_events(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        event_type: Optional[str] = None,
        impact_level: Optional[str] = None
    ) -> Dict:
        """
        Get event correlation data.
        
        Args:
            start_date: Start date filter
            end_date: End date filter
            event_type: Filter by event type
            impact_level: Filter by impact level (High, Medium, Low)
            
        Returns:
            Dictionary with event data
        """
        try:
            # Load events if not cached
            if self._events_cache is None:
                self.logger.info("Loading event data...")
                events_path = self.data_dir / "external" / "key_events.csv"
                
                if not events_path.exists():
                    raise DataServiceError(f"Events file not found: {events_path}")
                
                events = pd.read_csv(events_path)
                events['Event_Date'] = pd.to_datetime(events['Event_Date'])
                self._events_cache = events
            
            events = self._events_cache.copy()
            
            # Apply filters
            if start_date:
                events = events[events['Event_Date'] >= pd.to_datetime(start_date)]
            if end_date:
                events = events[events['Event_Date'] <= pd.to_datetime(end_date)]
            if event_type:
                events = events[events['Event_Type'] == event_type]
            if impact_level:
                events = events[events['Impact_Level'] == impact_level]
            
            # Convert to JSON-serializable format
            events_list = events.to_dict('records')
            for event in events_list:
                if isinstance(event['Event_Date'], pd.Timestamp):
                    event['Event_Date'] = event['Event_Date'].isoformat()
            
            result = {
                'events': events_list,
                'count': len(events),
                'filters': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'event_type': event_type,
                    'impact_level': impact_level
                }
            }
            
            self.logger.info(f"Returned {len(events)} events")
            return result
            
        except Exception as e:
            error_msg = f"Error loading events: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise DataServiceError(error_msg) from e
    
    def get_summary_statistics(self) -> Dict:
        """
        Get summary statistics from analysis.
        
        Returns:
            Dictionary with summary statistics
        """
        try:
            stats_file = self.reports_dir / "summary_statistics.csv"
            
            if stats_file.exists():
                stats = pd.read_csv(stats_file)
                return stats.to_dict('records')[0] if len(stats) > 0 else {}
            
            return {}
            
        except Exception as e:
            self.logger.warning(f"Error loading summary statistics: {e}")
            return {}
    
    def get_volatility_analysis(self) -> Dict:
        """
        Get volatility analysis results.
        
        Returns:
            Dictionary with volatility statistics
        """
        try:
            vol_file = self.reports_dir / "volatility_analysis.csv"
            
            if vol_file.exists():
                vol_data = pd.read_csv(vol_file)
                return vol_data.to_dict('records')[0] if len(vol_data) > 0 else {}
            
            return {}
            
        except Exception as e:
            self.logger.warning(f"Error loading volatility analysis: {e}")
            return {}
