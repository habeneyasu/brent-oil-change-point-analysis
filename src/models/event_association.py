"""
Event Association Module

This module provides functionality to associate detected change points
with key events and quantify their impact.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class EventAssociationError(Exception):
    """Custom exception for event association errors."""
    pass


class EventAssociator:
    """
    Class for associating change points with events and quantifying impacts.
    """
    
    def __init__(self, events_path: Optional[Path] = None):
        """
        Initialize the event associator.
        
        Args:
            events_path: Path to events CSV file. If None, uses default path.
        """
        if events_path is None:
            project_root = Path(__file__).parent.parent.parent
            events_path = project_root / "data" / "external" / "key_events.csv"
        
        self.events_path = Path(events_path)
        self.events: Optional[pd.DataFrame] = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        self._load_events()
    
    def _load_events(self) -> None:
        """Load events from CSV file."""
        try:
            if not self.events_path.exists():
                raise EventAssociationError(f"Events file not found: {self.events_path}")
            
            self.events = pd.read_csv(self.events_path)
            self.events['Event_Date'] = pd.to_datetime(self.events['Event_Date'])
            self.events = self.events.sort_values('Event_Date').reset_index(drop=True)
            
            self.logger.info(f"Loaded {len(self.events)} events from {self.events_path}")
            
        except Exception as e:
            error_msg = f"Error loading events: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise EventAssociationError(error_msg) from e
    
    def find_nearby_events(
        self,
        change_point_date: pd.Timestamp,
        window_days: int = 90
    ) -> pd.DataFrame:
        """
        Find events near a change point date.
        
        Args:
            change_point_date: Date of the change point
            window_days: Number of days before/after to search (default: 90)
            
        Returns:
            DataFrame with events within the window
        """
        try:
            if self.events is None:
                raise EventAssociationError("Events not loaded")
            
            # Calculate date range
            start_date = change_point_date - timedelta(days=window_days)
            end_date = change_point_date + timedelta(days=window_days)
            
            # Filter events
            nearby = self.events[
                (self.events['Event_Date'] >= start_date) &
                (self.events['Event_Date'] <= end_date)
            ].copy()
            
            # Calculate days difference
            nearby['Days_Difference'] = (nearby['Event_Date'] - change_point_date).dt.days
            nearby['Days_Abs'] = nearby['Days_Difference'].abs()
            
            # Sort by proximity
            nearby = nearby.sort_values('Days_Abs').reset_index(drop=True)
            
            return nearby
            
        except Exception as e:
            error_msg = f"Error finding nearby events: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise EventAssociationError(error_msg) from e
    
    def associate_change_point(
        self,
        change_point_date: pd.Timestamp,
        mu1: float,
        mu2: float,
        price_before: Optional[float] = None,
        price_after: Optional[float] = None,
        window_days: int = 90
    ) -> Dict:
        """
        Associate a change point with events and quantify impact.
        
        Args:
            change_point_date: Date of the change point
            mu1: Mean before change point (log returns)
            mu2: Mean after change point (log returns)
            price_before: Average price before change point (optional, for USD conversion)
            price_after: Average price after change point (optional, for USD conversion)
            window_days: Window to search for events
            
        Returns:
            Dictionary with association results and impact quantification
        """
        try:
            # Find nearby events
            nearby_events = self.find_nearby_events(change_point_date, window_days)
            
            # Calculate impact in log returns
            impact_log = mu2 - mu1
            impact_percent = (np.exp(impact_log) - 1) * 100
            
            # If prices provided, calculate USD impact
            impact_usd = None
            if price_before is not None and price_after is not None:
                impact_usd = price_after - price_before
            
            # Get closest event
            closest_event = None
            if len(nearby_events) > 0:
                closest_event = nearby_events.iloc[0].to_dict()
            
            # Format association results
            association = {
                'change_point_date': change_point_date,
                'mu1': mu1,
                'mu2': mu2,
                'impact_log': impact_log,
                'impact_percent': impact_percent,
                'impact_usd': impact_usd,
                'price_before': price_before,
                'price_after': price_after,
                'nearby_events': nearby_events.to_dict('records') if len(nearby_events) > 0 else [],
                'closest_event': closest_event,
                'window_days': window_days
            }
            
            return association
            
        except Exception as e:
            error_msg = f"Error associating change point: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise EventAssociationError(error_msg) from e
    
    def format_impact_statement(
        self,
        association: Dict,
        event_name: Optional[str] = None
    ) -> str:
        """
        Format a quantitative impact statement.
        
        Args:
            association: Association dictionary from associate_change_point
            event_name: Optional event name to include
            
        Returns:
            Formatted impact statement
        """
        try:
            cp_date = association['change_point_date']
            mu1 = association['mu1']
            mu2 = association['mu2']
            impact_percent = association['impact_percent']
            
            # Format date
            date_str = cp_date.strftime('%B %d, %Y')
            
            # Build statement
            if event_name:
                statement = (
                    f"Following the {event_name} around {date_str}, "
                    f"the model detects a change point"
                )
            else:
                statement = (
                    f"On {date_str}, "
                    f"the model detects a change point"
                )
            
            # Add price change if available
            if association['price_before'] is not None and association['price_after'] is not None:
                price_before = association['price_before']
                price_after = association['price_after']
                statement += (
                    f", with the average daily price shifting from "
                    f"${price_before:.2f} to ${price_after:.2f}"
                )
            
            # Add percentage change
            direction = "increase" if impact_percent > 0 else "decrease"
            statement += f", a {direction} of {abs(impact_percent):.2f}%."
            
            return statement
            
        except Exception as e:
            error_msg = f"Error formatting impact statement: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise EventAssociationError(error_msg) from e
