"""
Task 2: Interpret Model Output

This script interprets the Bayesian change point model results:
1. Check for Convergence using pm.summary() and trace plots
2. Identify the Change Point by plotting posterior distribution of tau
3. Quantify the Impact by plotting posterior distributions and making probabilistic statements
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import arviz as az

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from data_processing.load_data import BrentOilDataLoader
from models.change_point_model import BayesianChangePointModel
from visualization.change_point_plots import ChangePointVisualizer
from utils.config import setup_logging

# Setup logging
logger = setup_logging(log_level="INFO")

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


def main():
    """Main execution function for interpreting model output."""
    logger.info("=" * 80)
    logger.info("Task 2: Interpret Model Output")
    logger.info("=" * 80)
    
    # Load data and compute returns
    logger.info("\nLoading data and computing returns...")
    loader = BrentOilDataLoader()
    data_df = loader.load()
    returns = loader.compute_returns(method='log')
    
    logger.info(f"   Data shape: {len(returns)} observations")
    
    # Build and sample model (or load existing trace)
    logger.info("\n" + "=" * 80)
    logger.info("Building and Sampling Model")
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
    
    # ========================================================================
    # STEP 1: Check for Convergence
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("STEP 1: Check for Convergence")
    logger.info("=" * 80)
    
    logger.info("\n1.1 Using pm.summary() to check R-hat values...")
    convergence = cp_model.check_convergence()
    
    summary = convergence['summary']
    logger.info("\n   Summary Statistics:")
    logger.info(f"\n{summary.to_string()}")
    
    # Check R-hat values
    if convergence['converged']:
        logger.info("\n   ✅ CONVERGENCE: All R-hat values < 1.01")
        logger.info("   The model has converged successfully!")
    else:
        logger.warning("\n   ⚠️ CONVERGENCE WARNING: Some R-hat values >= 1.01")
        logger.warning("   The model may not have converged. Consider:")
        logger.warning("   - Running more iterations")
        logger.warning("   - Checking for divergent transitions")
        logger.warning("   - Adjusting model priors")
    
    # Display R-hat values
    if convergence['r_hat']:
        logger.info("\n   R-hat values (should be < 1.01):")
        for var, rhat in convergence['r_hat'].items():
            status = "✅" if rhat < 1.01 else "⚠️"
            logger.info(f"      {status} {var}: {rhat:.4f}")
    
    # Display ESS
    if convergence['ess_bulk']:
        logger.info("\n   Effective Sample Size (ESS):")
        for var, ess in convergence['ess_bulk'].items():
            logger.info(f"      {var}: {ess:.0f}")
    
    # Plot trace plots
    logger.info("\n1.2 Plotting trace plots for visual convergence check...")
    visualizer = ChangePointVisualizer()
    
    # Let the plot_trace function handle variable name resolution
    # It will automatically find variables with or without prefixes
    fig = visualizer.plot_trace(
        trace,
        var_names=None,  # None means use all available variables
        title="MCMC Trace Plots - Convergence Diagnostics"
    )
    plt.close(fig)
    logger.info("   ✅ Trace plots saved to reports/trace_plots.png")
    
    logger.info("\n   📊 Trace Plot Interpretation:")
    logger.info("      - Left plots: Should show 'fuzzy caterpillars' (well-mixed chains)")
    logger.info("      - Right plots: Should show stable distributions")
    logger.info("      - No trends or drifts indicate convergence")
    
    # ========================================================================
    # STEP 2: Identify the Change Point
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("STEP 2: Identify the Change Point")
    logger.info("=" * 80)
    
    logger.info("\n2.1 Extracting change point posterior...")
    cp_results = cp_model.get_change_point_posterior()
    
    logger.info(f"\n   Change Point Statistics:")
    logger.info(f"      Most probable (mode): Observation {cp_results['tau_mode']}")
    logger.info(f"      Median: Observation {cp_results['tau_median']}")
    logger.info(f"      Mean: {cp_results['tau_mean']:.2f}")
    logger.info(f"      Std Dev: {cp_results['tau_std']:.2f}")
    logger.info(f"      95% Credible Interval: [{cp_results['tau_lower_95']}, {cp_results['tau_upper_95']}]")
    
    if cp_results['change_point_date']:
        logger.info(f"      Date: {cp_results['change_point_date']}")
    
    # Plot posterior distribution of tau
    logger.info("\n2.2 Plotting posterior distribution of tau...")
    fig = visualizer.plot_tau_posterior(
        cp_results['tau_samples'],
        title="Posterior Distribution of Change Point (τ)"
    )
    plt.close(fig)
    logger.info("   ✅ Tau posterior plot saved to reports/tau_posterior.png")
    
    # Interpret the distribution
    tau_std = cp_results['tau_std']
    tau_range = cp_results['tau_upper_95'] - cp_results['tau_lower_95']
    n_obs = len(returns)
    uncertainty_pct = (tau_range / n_obs) * 100
    
    logger.info("\n   📊 Change Point Interpretation:")
    if tau_std < n_obs * 0.05:  # Less than 5% of data
        logger.info("      ✅ HIGH CERTAINTY: Sharp, narrow peak in posterior")
        logger.info("      The change point location is well-identified")
    elif tau_std < n_obs * 0.15:  # Less than 15% of data
        logger.info("      ⚠️ MODERATE CERTAINTY: Moderate peak in posterior")
        logger.info("      The change point location has some uncertainty")
    else:
        logger.info("      ⚠️ LOW CERTAINTY: Wide, flat posterior distribution")
        logger.info("      The change point location is uncertain")
    
    logger.info(f"      Uncertainty: {uncertainty_pct:.1f}% of data range")
    
    # ========================================================================
    # STEP 3: Quantify the Impact
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("STEP 3: Quantify the Impact")
    logger.info("=" * 80)
    
    logger.info("\n3.1 Extracting parameter posteriors...")
    param_results = cp_model.get_parameter_posteriors()
    
    logger.info(f"\n   Parameter Estimates:")
    logger.info(f"      μ₁ (before): {param_results['mu1_mean']:.6f}")
    logger.info(f"         95% CI: [{param_results['mu1_lower_95']:.6f}, {param_results['mu1_upper_95']:.6f}]")
    logger.info(f"      μ₂ (after): {param_results['mu2_mean']:.6f}")
    logger.info(f"         95% CI: [{param_results['mu2_lower_95']:.6f}, {param_results['mu2_upper_95']:.6f}]")
    logger.info(f"      σ: {param_results['sigma_mean']:.6f}")
    logger.info(f"         95% CI: [{param_results['sigma_lower_95']:.6f}, {param_results['sigma_upper_95']:.6f}]")
    
    logger.info(f"\n   Impact Quantification:")
    logger.info(f"      Mean change: {param_results['impact_mean']:.6f}")
    logger.info(f"      Percentage change: {param_results['impact_percent']:.2f}%")
    logger.info(f"      95% Credible Interval: [{param_results['impact_lower_95']:.6f}, {param_results['impact_upper_95']:.6f}]")
    
    # Plot parameter posteriors
    logger.info("\n3.2 Plotting posterior distributions of parameters...")
    fig = visualizer.plot_parameter_posteriors(
        param_results['mu1_samples'],
        param_results['mu2_samples'],
        param_results['sigma_samples'],
        title="Posterior Distributions of Model Parameters"
    )
    plt.close(fig)
    logger.info("   ✅ Parameter posteriors plot saved to reports/parameter_posteriors.png")
    
    # Make probabilistic statements
    logger.info("\n3.3 Probabilistic Statements:")
    
    # Probability that impact is positive
    impact_samples = param_results['impact_samples']
    prob_positive = np.mean(impact_samples > 0) * 100
    prob_negative = np.mean(impact_samples < 0) * 100
    
    logger.info(f"\n   📊 Impact Direction:")
    logger.info(f"      Probability of increase: {prob_positive:.1f}%")
    logger.info(f"      Probability of decrease: {prob_negative:.1f}%")
    
    if prob_positive > 95:
        logger.info("      ✅ STRONG EVIDENCE: Change point associated with increase")
    elif prob_positive > 80:
        logger.info("      ⚠️ MODERATE EVIDENCE: Change point likely associated with increase")
    elif prob_negative > 95:
        logger.info("      ✅ STRONG EVIDENCE: Change point associated with decrease")
    elif prob_negative > 80:
        logger.info("      ⚠️ MODERATE EVIDENCE: Change point likely associated with decrease")
    else:
        logger.info("      ⚠️ UNCERTAIN: Direction of change is uncertain")
    
    # Magnitude statements
    impact_mean = param_results['impact_mean']
    impact_std = param_results['impact_std']
    
    logger.info(f"\n   📊 Impact Magnitude:")
    logger.info(f"      Mean impact: {impact_mean:.6f} (log returns)")
    logger.info(f"      Standard deviation: {impact_std:.6f}")
    
    # Convert to percentage for interpretation
    if abs(impact_mean) > 0.01:
        logger.info(f"      This represents approximately {abs(param_results['impact_percent']):.2f}% change in returns")
    
    # ========================================================================
    # Summary
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("INTERPRETATION SUMMARY")
    logger.info("=" * 80)
    
    logger.info("\n✅ Convergence:")
    logger.info(f"   Status: {'Converged' if convergence['converged'] else 'May not have converged'}")
    logger.info(f"   All R-hat < 1.01: {convergence['converged']}")
    
    logger.info("\n✅ Change Point:")
    logger.info(f"   Location: Observation {cp_results['tau_median']}")
    logger.info(f"   Certainty: {'High' if tau_std < n_obs * 0.05 else 'Moderate' if tau_std < n_obs * 0.15 else 'Low'}")
    logger.info(f"   95% CI: [{cp_results['tau_lower_95']}, {cp_results['tau_upper_95']}]")
    
    logger.info("\n✅ Impact:")
    logger.info(f"   Mean change: {param_results['impact_mean']:.6f}")
    logger.info(f"   Percentage: {param_results['impact_percent']:.2f}%")
    logger.info(f"   Direction: {'Increase' if prob_positive > 50 else 'Decrease'} ({max(prob_positive, prob_negative):.1f}% probability)")
    
    logger.info("\n📁 All visualizations saved to reports/ directory:")
    logger.info("   - trace_plots.png")
    logger.info("   - tau_posterior.png")
    logger.info("   - parameter_posteriors.png")
    
    logger.info("\n" + "=" * 80)
    logger.info("Model interpretation completed successfully!")
    logger.info("=" * 80)
    
    return {
        'trace': trace,
        'convergence': convergence,
        'cp_results': cp_results,
        'param_results': param_results
    }


if __name__ == "__main__":
    results = main()
