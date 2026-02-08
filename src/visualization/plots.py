"""
Visualization module for Brent oil price analysis.

This module provides classes and functions for creating professional
visualizations of time series data, trends, and statistical properties.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class VisualizationError(Exception):
    """Custom exception for visualization errors."""
    pass


class TimeSeriesVisualizer:
    """
    Class for creating visualizations of time series data.
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save plots. If None, uses reports/ directory.
        """
        if output_dir is None:
            project_root = Path(__file__).parent.parent.parent
            output_dir = project_root / "reports"
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def plot_price_series(
        self, 
        data: pd.DataFrame,
        title: str = "Brent Oil Price Time Series",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """
        Plot the raw price series over time.
        
        Args:
            data: DataFrame with Date index and Price column
            title: Plot title
            save_path: Path to save figure. If None, auto-generates name.
            
        Returns:
            matplotlib Figure object
        """
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(data.index, data['Price'], linewidth=1.5, color='#2E86AB')
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Price (USD per barrel)', fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            
            # Format x-axis dates
            fig.autofmt_xdate()
            
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "price_series.png"
            else:
                save_path = Path(save_path)
            
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved price series plot to {save_path}")
            
            return fig
            
        except Exception as e:
            error_msg = f"Error plotting price series: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise VisualizationError(error_msg) from e
    
    def plot_returns(
        self,
        returns: pd.Series,
        title: str = "Log Returns Time Series",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """
        Plot log returns over time.
        
        Args:
            returns: Series of returns
            title: Plot title
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(returns.index, returns.values, linewidth=0.8, color='#A23B72', alpha=0.7)
            ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Log Returns', fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            
            fig.autofmt_xdate()
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "returns_series.png"
            else:
                save_path = Path(save_path)
            
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved returns plot to {save_path}")
            
            return fig
            
        except Exception as e:
            error_msg = f"Error plotting returns: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise VisualizationError(error_msg) from e
    
    def plot_volatility(
        self,
        volatility: pd.Series,
        title: str = "Rolling Volatility (30-day window)",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """
        Plot rolling volatility over time.
        
        Args:
            volatility: Series of rolling volatility
            title: Plot title
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(volatility.index, volatility.values, linewidth=1.5, color='#F18F01')
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Volatility (Std Dev)', fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            
            fig.autofmt_xdate()
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "volatility_series.png"
            else:
                save_path = Path(save_path)
            
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved volatility plot to {save_path}")
            
            return fig
            
        except Exception as e:
            error_msg = f"Error plotting volatility: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise VisualizationError(error_msg) from e
    
    def plot_distribution(
        self,
        data: pd.Series,
        title: str = "Price Distribution",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """
        Plot distribution of prices or returns.
        
        Args:
            data: Series to plot
            title: Plot title
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Histogram
            ax1.hist(data.values, bins=50, color='#6A994E', alpha=0.7, edgecolor='black')
            ax1.set_xlabel('Value', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
            ax1.set_title(f'{title} - Histogram', fontsize=12, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            
            # Q-Q plot
            from scipy import stats
            stats.probplot(data.values, dist="norm", plot=ax2)
            ax2.set_title(f'{title} - Q-Q Plot', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            
            plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / f"distribution_{title.lower().replace(' ', '_')}.png"
            else:
                save_path = Path(save_path)
            
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved distribution plot to {save_path}")
            
            return fig
            
        except Exception as e:
            error_msg = f"Error plotting distribution: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise VisualizationError(error_msg) from e
    
    def plot_events_overlay(
        self,
        data: pd.DataFrame,
        events: pd.DataFrame,
        title: str = "Brent Oil Prices with Key Events",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """
        Plot price series with event markers.
        
        Args:
            data: DataFrame with Date index and Price column
            events: DataFrame with Event_Date and Event_Description columns
            title: Plot title
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        try:
            fig, ax = plt.subplots(figsize=(16, 8))
            
            # Plot price series
            ax.plot(data.index, data['Price'], linewidth=1.5, color='#2E86AB', label='Price')
            
            # Add event markers
            events['Event_Date'] = pd.to_datetime(events['Event_Date'])
            
            for _, event in events.iterrows():
                event_date = event['Event_Date']
                if event_date in data.index:
                    price_at_event = data.loc[event_date, 'Price']
                    ax.scatter(
                        event_date, 
                        price_at_event, 
                        color='red', 
                        s=100, 
                        zorder=5,
                        alpha=0.7
                    )
                    ax.annotate(
                        event['Event_Description'][:30] + '...' if len(event['Event_Description']) > 30 else event['Event_Description'],
                        xy=(event_date, price_at_event),
                        xytext=(10, 10),
                        textcoords='offset points',
                        fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                    )
            
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Price (USD per barrel)', fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            fig.autofmt_xdate()
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "price_with_events.png"
            else:
                save_path = Path(save_path)
            
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved events overlay plot to {save_path}")
            
            return fig
            
        except Exception as e:
            error_msg = f"Error plotting events overlay: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise VisualizationError(error_msg) from e
