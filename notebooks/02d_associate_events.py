"""
Task 2: Associate Changes with Causes and Quantify Impact

This script:
1. Compares detected change point dates with key events
2. Formulates hypotheses about which events triggered shifts
3. Quantifies the impact for each major change point
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import timedelta

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from data_processing.load_data import BrentOilDataLoader
from models.change_point_model import BayesianChangePointModel
from models.event_association import EventAssociator
from utils.config import setup_logging

# Setup logging
logger = setup_logging(log_level="INFO")


def main():
    """Main execution function for event association."""
    logger.info("=" * 80)
    logger.info("Task 2: Associate Changes with Causes and Quantify Impact")
    logger.info("=" * 80)
    
    # Load data
    logger.info("\nLoading data...")
    loader = BrentOilDataLoader()
    data_df = loader.load()
    data_df['Date'] = pd.to_datetime(data_df['Date'])
    data_indexed = data_df.set_index('Date')
    
    # Compute returns
    returns = loader.compute_returns(method='log')
    returns_indexed = returns.to_frame('Returns')
    returns_indexed.index = data_indexed.index[1:]
    
    logger.info(f"   Data: {len(data_df)} observations")
    logger.info(f"   Returns: {len(returns)} observations")
    
    # Build and sample model
    logger.info("\n" + "=" * 80)
    logger.info("Building and Sampling Change Point Model")
    logger.info("=" * 80)
    
    cp_model = BayesianChangePointModel(returns, model_name="brent_oil_cp")
    cp_model.build_model()
    
    logger.info("\nRunning MCMC sampling...")
    logger.info("(This may take several minutes...)")
    
    trace = cp_model.sample(
        draws=2000,
        tune=1000,
        chains=4,
        target_accept=0.95,
        random_seed=42
    )
    
    logger.info("✅ Sampling completed!")
    
    # Extract results
    logger.info("\nExtracting change point and parameter results...")
    cp_results = cp_model.get_change_point_posterior()
    param_results = cp_model.get_parameter_posteriors()
    
    # Initialize event associator
    logger.info("\nInitializing event associator...")
    associator = EventAssociator()
    
    # ========================================================================
    # Associate Change Point with Events
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("ASSOCIATING CHANGE POINT WITH EVENTS")
    logger.info("=" * 80)
    
    # Get change point date
    # Try to get from results, otherwise convert observation index
    cp_date = None
    if cp_results.get('change_point_date') and pd.notna(cp_results['change_point_date']):
        try:
            cp_date = pd.to_datetime(cp_results['change_point_date'])
        except:
            cp_date = None
    
    if cp_date is None:
        # Convert observation index to date
        cp_obs = int(cp_results['tau_median'])
        # Ensure we don't go out of bounds
        if cp_obs < len(returns_indexed):
            cp_date = pd.to_datetime(returns_indexed.index[cp_obs])
        elif cp_obs < len(data_indexed):
            # Try using data_indexed if returns_indexed is too short
            cp_date = pd.to_datetime(data_indexed.index[cp_obs])
        else:
            # Fallback: use the last date
            cp_date = pd.to_datetime(data_indexed.index[-1])
            logger.warning(f"Change point observation {cp_obs} out of bounds, using last date")
    
    # Ensure cp_date is a datetime/Timestamp
    if not isinstance(cp_date, pd.Timestamp):
        cp_date = pd.to_datetime(cp_date)
    
    logger.info(f"\nChange Point Detected:")
    logger.info(f"   Date: {cp_date.strftime('%B %d, %Y')}")
    logger.info(f"   Observation: {cp_results['tau_median']}")
    logger.info(f"   95% Credible Interval: [{cp_results['tau_lower_95']}, {cp_results['tau_upper_95']}]")
    
    # Find nearby events
    logger.info(f"\nSearching for events within 90 days of change point...")
    nearby_events = associator.find_nearby_events(cp_date, window_days=90)
    
    logger.info(f"   Found {len(nearby_events)} events within window")
    
    if len(nearby_events) > 0:
        logger.info("\n   Nearby Events:")
        for idx, event in nearby_events.head(5).iterrows():
            days_diff = event['Days_Difference']
            direction = "before" if days_diff < 0 else "after"
            logger.info(
                f"      - {event['Event_Description'][:50]}... "
                f"({abs(days_diff)} days {direction})"
            )
    
    # Calculate average prices before and after
    logger.info("\nCalculating average prices before and after change point...")
    cp_obs = cp_results['tau_median']
    
    # Get prices before and after
    prices_before = data_indexed.iloc[:cp_obs]['Price']
    prices_after = data_indexed.iloc[cp_obs:]['Price']
    
    avg_price_before = prices_before.mean()
    avg_price_after = prices_after.mean()
    
    logger.info(f"   Average price before: ${avg_price_before:.2f}")
    logger.info(f"   Average price after: ${avg_price_after:.2f}")
    
    # Associate change point with events
    logger.info("\nAssociating change point with events...")
    association = associator.associate_change_point(
        change_point_date=cp_date,
        mu1=param_results['mu1_mean'],
        mu2=param_results['mu2_mean'],
        price_before=avg_price_before,
        price_after=avg_price_after,
        window_days=90
    )
    
    # ========================================================================
    # Formulate Hypotheses
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("FORMULATING HYPOTHESES")
    logger.info("=" * 80)
    
    if association['closest_event']:
        closest = association['closest_event']
        days_diff = closest['Days_Difference']
        
        logger.info(f"\nClosest Event:")
        logger.info(f"   Event: {closest['Event_Description']}")
        logger.info(f"   Date: {closest['Event_Date'].strftime('%B %d, %Y')}")
        logger.info(f"   Type: {closest['Event_Type']}")
        logger.info(f"   Region: {closest['Region']}")
        logger.info(f"   Impact Level: {closest['Impact_Level']}")
        logger.info(f"   Days from change point: {abs(days_diff)} days {'before' if days_diff < 0 else 'after'}")
        
        # Formulate hypothesis
        logger.info("\n   📊 Hypothesis:")
        if abs(days_diff) <= 30:
            confidence = "HIGH"
            logger.info(f"      {confidence} CONFIDENCE: The {closest['Event_Type']} likely triggered the change point.")
            logger.info(f"      The event occurred {abs(days_diff)} days {'before' if days_diff < 0 else 'after'} the detected change point.")
        elif abs(days_diff) <= 60:
            confidence = "MODERATE"
            logger.info(f"      {confidence} CONFIDENCE: The {closest['Event_Type']} may have contributed to the change point.")
            logger.info(f"      The event occurred {abs(days_diff)} days {'before' if days_diff < 0 else 'after'} the detected change point.")
        else:
            confidence = "LOW"
            logger.info(f"      {confidence} CONFIDENCE: The {closest['Event_Type']} may be related, but timing suggests other factors.")
            logger.info(f"      The event occurred {abs(days_diff)} days {'before' if days_diff < 0 else 'after'} the detected change point.")
        
        # Consider other nearby events
        if len(nearby_events) > 1:
            logger.info(f"\n   Other Events in Window ({len(nearby_events)} total):")
            logger.info("      Multiple events may have contributed to the change point.")
            logger.info("      Consider cumulative effects or market anticipation.")
    else:
        logger.info("\n   ⚠️ No events found within 90 days of change point.")
        logger.info("      The change point may be due to:")
        logger.info("      - Gradual market forces")
        logger.info("      - Events not in our dataset")
        logger.info("      - Market anticipation of future events")
    
    # ========================================================================
    # Quantify the Impact
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("QUANTIFYING IMPACT")
    logger.info("=" * 80)
    
    logger.info(f"\nImpact Statistics:")
    logger.info(f"   Mean log return before: {association['mu1']:.6f}")
    logger.info(f"   Mean log return after: {association['mu2']:.6f}")
    logger.info(f"   Change in log returns: {association['impact_log']:.6f}")
    logger.info(f"   Percentage change: {association['impact_percent']:.2f}%")
    
    if association['price_before'] and association['price_after']:
        logger.info(f"   Average price before: ${association['price_before']:.2f}")
        logger.info(f"   Average price after: ${association['price_after']:.2f}")
        logger.info(f"   Price change: ${association['impact_usd']:.2f}")
    
    # Format impact statement
    logger.info("\n" + "=" * 80)
    logger.info("QUANTITATIVE IMPACT STATEMENTS")
    logger.info("=" * 80)
    
    if association['closest_event']:
        event_name = association['closest_event']['Event_Description']
        statement = associator.format_impact_statement(association, event_name)
    else:
        statement = associator.format_impact_statement(association)
    
    logger.info("\n📊 Formatted Impact Statement:")
    logger.info(f"\n   {statement}\n")
    
    # Additional impact details
    logger.info("   Additional Details:")
    logger.info(f"   - Change point detected on: {cp_date.strftime('%B %d, %Y')}")
    logger.info(f"   - 95% Credible Interval for change point: [{cp_results['tau_lower_95']}, {cp_results['tau_upper_95']}] observations")
    logger.info(f"   - Statistical significance: {'High' if cp_results['tau_std'] < 100 else 'Moderate' if cp_results['tau_std'] < 500 else 'Low'} certainty")
    
    # Save results
    logger.info("\n" + "=" * 80)
    logger.info("Saving Results")
    logger.info("=" * 80)
    
    results_dir = project_root / "reports"
    results_dir.mkdir(exist_ok=True)
    
    # Save association results
    association_df = pd.DataFrame([{
        'change_point_date': cp_date,
        'change_point_obs': cp_results['tau_median'],
        'mu1': association['mu1'],
        'mu2': association['mu2'],
        'impact_percent': association['impact_percent'],
        'price_before': association['price_before'],
        'price_after': association['price_after'],
        'impact_usd': association['impact_usd'],
        'closest_event': association['closest_event']['Event_Description'] if association['closest_event'] else None,
        'closest_event_date': association['closest_event']['Event_Date'] if association['closest_event'] else None,
        'days_difference': association['closest_event']['Days_Difference'] if association['closest_event'] else None,
        'impact_statement': statement
    }])
    
    association_df.to_csv(results_dir / "change_point_association.csv", index=False)
    logger.info("   ✅ Results saved to reports/change_point_association.csv")
    
    # Save nearby events
    if len(nearby_events) > 0:
        nearby_events.to_csv(results_dir / "nearby_events.csv", index=False)
        logger.info("   ✅ Nearby events saved to reports/nearby_events.csv")
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ Event association and impact quantification completed!")
    logger.info("=" * 80)
    
    return {
        'association': association,
        'statement': statement,
        'nearby_events': nearby_events
    }


if __name__ == "__main__":
    results = main()
