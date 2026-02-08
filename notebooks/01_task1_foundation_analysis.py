"""
Task 1: Laying the Foundation for Analysis

This script performs comprehensive data analysis and documentation
for the Brent oil price change point analysis project.

It includes:
- Data loading and preprocessing
- Time series property analysis (trend, stationarity, volatility)
- Event data compilation
- Visualization generation
- Documentation of assumptions and limitations
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from data_processing.load_data import BrentOilDataLoader
from data_processing.preprocess import TimeSeriesAnalyzer
from visualization.plots import TimeSeriesVisualizer
from utils.config import setup_logging

# Setup logging
logger = setup_logging(log_level="INFO")


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("Task 1: Laying the Foundation for Analysis")
    logger.info("=" * 80)
    
    # Initialize components
    logger.info("\n1. Loading data...")
    loader = BrentOilDataLoader()
    data = loader.load()
    
    logger.info(f"   Loaded {len(data)} records")
    logger.info(f"   Date range: {data['Date'].min()} to {data['Date'].max()}")
    
    # Compute returns
    logger.info("\n2. Computing returns...")
    returns = loader.compute_returns(method='log')
    logger.info(f"   Computed {len(returns)} log returns")
    
    # Initialize analyzer
    logger.info("\n3. Initializing time series analyzer...")
    analyzer = TimeSeriesAnalyzer(data)
    
    # Trend analysis
    logger.info("\n4. Analyzing trends...")
    trend_results = analyzer.analyze_trend()
    logger.info(f"   Trend direction: {trend_results['trend_direction']}")
    logger.info(f"   R-squared: {trend_results['r_squared']:.4f}")
    logger.info(f"   P-value: {trend_results['p_value']:.4f}")
    logger.info(f"   Significant: {trend_results['is_significant']}")
    
    # Stationarity testing
    logger.info("\n5. Testing stationarity...")
    adf_results = analyzer.test_stationarity(method='adf')
    logger.info(f"   ADF test: {adf_results['interpretation']}")
    logger.info(f"   ADF p-value: {adf_results['p_value']:.4f}")
    
    kpss_results = analyzer.test_stationarity(method='kpss')
    logger.info(f"   KPSS test: {kpss_results['interpretation']}")
    logger.info(f"   KPSS p-value: {kpss_results['p_value']:.4f}")
    
    # Volatility analysis
    logger.info("\n6. Analyzing volatility...")
    volatility_results = analyzer.analyze_volatility(window=30)
    logger.info(f"   Mean volatility: {volatility_results['mean_volatility']:.4f}")
    logger.info(f"   Annualized volatility: {volatility_results['annualized_volatility']:.2%}")
    logger.info(f"   Volatility clustering: {volatility_results['volatility_clustering']['interpretation']}")
    
    # Summary statistics
    logger.info("\n7. Computing summary statistics...")
    summary_stats = analyzer.get_summary_statistics()
    logger.info("\n   Summary Statistics:")
    logger.info(f"\n{summary_stats.to_string()}")
    
    # Load event data
    logger.info("\n8. Loading event data...")
    events_path = project_root / "data" / "external" / "key_events.csv"
    events = pd.read_csv(events_path)
    events['Event_Date'] = pd.to_datetime(events['Event_Date'])
    logger.info(f"   Loaded {len(events)} key events")
    
    # Create visualizations
    logger.info("\n9. Creating visualizations...")
    visualizer = TimeSeriesVisualizer()
    
    # Price series
    data_indexed = data.set_index('Date')
    visualizer.plot_price_series(data_indexed)
    
    # Returns
    returns_indexed = returns.to_frame('Returns')
    returns_indexed.index = data_indexed.index[1:]  # Align with dates
    visualizer.plot_returns(returns_indexed['Returns'])
    
    # Volatility
    visualizer.plot_volatility(volatility_results['rolling_volatility'])
    
    # Distribution
    visualizer.plot_distribution(data['Price'], title="Price Distribution")
    visualizer.plot_distribution(returns, title="Returns Distribution")
    
    # Events overlay
    visualizer.plot_events_overlay(data_indexed, events)
    
    logger.info("   All visualizations saved to reports/ directory")
    
    # Save analysis results
    logger.info("\n10. Saving analysis results...")
    results_dir = project_root / "reports"
    results_dir.mkdir(exist_ok=True)
    
    # Save summary statistics
    summary_stats.to_csv(results_dir / "summary_statistics.csv", index=False)
    
    # Save trend analysis
    pd.DataFrame([trend_results]).to_csv(
        results_dir / "trend_analysis.csv", 
        index=False
    )
    
    # Save stationarity tests
    stationarity_df = pd.DataFrame([adf_results, kpss_results])
    stationarity_df.to_csv(
        results_dir / "stationarity_tests.csv", 
        index=False
    )
    
    # Save volatility analysis
    volatility_df = pd.DataFrame([{
        'mean_volatility': volatility_results['mean_volatility'],
        'annualized_volatility': volatility_results['annualized_volatility'],
        'min_volatility': volatility_results['min_volatility'],
        'max_volatility': volatility_results['max_volatility'],
        'mean_rolling_volatility': volatility_results['mean_rolling_volatility'],
        'volatility_clustering': volatility_results['volatility_clustering']['has_clustering']
    }])
    volatility_df.to_csv(results_dir / "volatility_analysis.csv", index=False)
    
    logger.info("   Analysis results saved to reports/ directory")
    
    logger.info("\n" + "=" * 80)
    logger.info("Task 1 analysis completed successfully!")
    logger.info("=" * 80)
    
    return {
        'data': data,
        'returns': returns,
        'trend_results': trend_results,
        'adf_results': adf_results,
        'kpss_results': kpss_results,
        'volatility_results': volatility_results,
        'summary_stats': summary_stats,
        'events': events
    }


if __name__ == "__main__":
    results = main()
