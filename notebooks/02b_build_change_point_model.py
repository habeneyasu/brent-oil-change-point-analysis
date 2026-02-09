"""
Task 2: Build and Run Bayesian Change Point Model

This script demonstrates building the Bayesian change point model in PyMC
following the exact specifications:
1. Define Switch Point (tau) as discrete uniform prior
2. Define Before and After Parameters (μ₁, μ₂)
3. Use Switch Function to select correct parameter
4. Define Likelihood with pm.Normal
5. Run MCMC Sampler
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from data_processing.load_data import BrentOilDataLoader
from models.change_point_model import BayesianChangePointModel
from utils.config import setup_logging

# Setup logging
logger = setup_logging(log_level="INFO")

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10


def build_model_manual(data: np.ndarray, n_obs: int):
    """
    Build the Bayesian change point model manually following specifications.
    
    This function demonstrates the exact model structure as specified:
    1. Define Switch Point (tau): discrete uniform prior
    2. Define Before and After Parameters: μ₁, μ₂
    3. Use Switch Function: pm.math.switch
    4. Define Likelihood: pm.Normal
    """
    logger.info("=" * 80)
    logger.info("Building Bayesian Change Point Model (Manual Implementation)")
    logger.info("=" * 80)
    
    with pm.Model(name="brent_oil_change_point") as model:
        # ====================================================================
        # STEP 1: Define the Switch Point (tau)
        # ====================================================================
        logger.info("\n1. Defining Switch Point (tau)...")
        logger.info("   - Discrete uniform prior over all possible days")
        logger.info(f"   - Lower bound: 1, Upper bound: {n_obs - 1}")
        
        tau = pm.DiscreteUniform(
            "tau",                    # Parameter name
            lower=1,                   # First possible change point
            upper=n_obs - 1,           # Last possible change point
            initval=n_obs // 2        # Initial value (middle of series)
        )
        
        logger.info(f"   ✅ tau defined: DiscreteUniform(1, {n_obs - 1})")
        
        # ====================================================================
        # STEP 2: Define "Before" and "After" Parameters
        # ====================================================================
        logger.info("\n2. Defining Before and After Parameters (μ₁, μ₂)...")
        logger.info("   - μ₁: Mean before change point")
        logger.info("   - μ₂: Mean after change point")
        
        # Priors for means before and after change point
        # Using Normal priors centered at data mean with wide variance
        data_mean = np.mean(data)
        data_std = np.std(data)
        
        mu1 = pm.Normal(
            "mu1",                    # Mean before change point
            mu=data_mean,              # Prior mean
            sigma=data_std * 2        # Prior standard deviation (wide)
        )
        
        mu2 = pm.Normal(
            "mu2",                    # Mean after change point
            mu=data_mean,             # Prior mean
            sigma=data_std * 2       # Prior standard deviation (wide)
        )
        
        logger.info(f"   ✅ μ₁ (mu1) defined: Normal(μ={data_mean:.2f}, σ={data_std*2:.2f})")
        logger.info(f"   ✅ μ₂ (mu2) defined: Normal(μ={data_mean:.2f}, σ={data_std*2:.2f})")
        
        # ====================================================================
        # STEP 3: Use Switch Function
        # ====================================================================
        logger.info("\n3. Using Switch Function (pm.math.switch)...")
        logger.info("   - Select μ₁ if time index < tau (before change point)")
        logger.info("   - Select μ₂ if time index >= tau (after change point)")
        
        # Create time indices
        time_indices = np.arange(n_obs)
        
        # Switch function: 
        # - If tau >= index (i.e., index < tau): use mu1 (before change point)
        # - If tau < index (i.e., index >= tau): use mu2 (after change point)
        mu = pm.math.switch(
            tau >= time_indices,  # Condition: True if before change point
            mu1,                  # Value if True (before change point)
            mu2                   # Value if False (after change point)
        )
        
        logger.info("   ✅ Switch function: mu = pm.math.switch(tau >= time_indices, mu1, mu2)")
        
        # ====================================================================
        # STEP 4: Define the Likelihood
        # ====================================================================
        logger.info("\n4. Defining Likelihood...")
        logger.info("   - pm.Normal distribution")
        logger.info("   - Mean determined by switch function")
        logger.info("   - Standard deviation as additional parameter")
        
        # Prior for standard deviation
        sigma = pm.HalfNormal(
            "sigma",                # Standard deviation
            sigma=data_std          # Prior scale
        )
        
        # Likelihood: connect model to data
        likelihood = pm.Normal(
            "likelihood",
            mu=mu,                  # Mean from switch function
            sigma=sigma,            # Standard deviation
            observed=data           # Observed data
        )
        
        logger.info("   ✅ Likelihood defined: pm.Normal(mu=mu, sigma=sigma, observed=data)")
        
        logger.info("\n" + "=" * 80)
        logger.info("Model structure complete!")
        logger.info("=" * 80)
        logger.info("\nModel Parameters:")
        logger.info("  - tau: Change point location (discrete uniform)")
        logger.info("  - mu1: Mean before change point (normal)")
        logger.info("  - mu2: Mean after change point (normal)")
        logger.info("  - sigma: Standard deviation (half-normal)")
        logger.info("  - mu: Switch function output (determines which mean to use)")
        logger.info("  - likelihood: Observed data (normal)")
    
    return model


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("Task 2: Build Bayesian Change Point Model")
    logger.info("=" * 80)
    
    # Load data
    logger.info("\nLoading data...")
    loader = BrentOilDataLoader()
    data_df = loader.load()
    
    # Use log returns for better stationarity
    logger.info("\nComputing log returns for modeling...")
    returns = loader.compute_returns(method='log')
    
    logger.info(f"   Data shape: {len(returns)} observations")
    logger.info(f"   Mean return: {returns.mean():.6f}")
    logger.info(f"   Std return: {returns.std():.6f}")
    
    # Convert to numpy array for modeling
    data_array = returns.values
    n_obs = len(data_array)
    
    # ========================================================================
    # Build Model (Manual Implementation)
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("BUILDING MODEL (Manual Implementation)")
    logger.info("=" * 80)
    
    model = build_model_manual(data_array, n_obs)
    
    # ========================================================================
    # Build Model (Using Class)
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("BUILDING MODEL (Using BayesianChangePointModel Class)")
    logger.info("=" * 80)
    
    cp_model = BayesianChangePointModel(returns, model_name="brent_oil_cp")
    model_class = cp_model.build_model()
    
    logger.info("   ✅ Model built using class method")
    
    # ========================================================================
    # STEP 5: Run the Sampler
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("STEP 5: Running MCMC Sampler")
    logger.info("=" * 80)
    
    logger.info("\nSampling parameters:")
    logger.info("  - Chains: 4")
    logger.info("  - Draws: 2000 per chain")
    logger.info("  - Tune steps: 1000 per chain")
    logger.info("  - Total samples: 8000")
    
    logger.info("\nStarting MCMC sampling...")
    logger.info("(This may take several minutes...)")
    
    # Run sampler
    trace = cp_model.sample(
        draws=2000,
        tune=1000,
        chains=4,
        target_accept=0.95,
        random_seed=42
    )
    
    logger.info("\n✅ MCMC sampling completed!")
    
    # ========================================================================
    # Check Convergence
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("Checking Convergence")
    logger.info("=" * 80)
    
    convergence = cp_model.check_convergence()
    
    if convergence['converged']:
        logger.info("\n✅ Model converged successfully!")
        logger.info("   All R-hat values < 1.01")
    else:
        logger.warning("\n⚠️ Model may not have converged")
        logger.warning("   Some R-hat values >= 1.01")
    
    # Display summary
    logger.info("\nParameter Summary:")
    logger.info(f"\n{convergence['summary']}")
    
    # ========================================================================
    # Extract Results
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("Extracting Change Point Results")
    logger.info("=" * 80)
    
    cp_results = cp_model.get_change_point_posterior()
    param_results = cp_model.get_parameter_posteriors()
    
    logger.info(f"\nChange Point Detection:")
    logger.info(f"  - Most probable location: Observation {cp_results['tau_mode']}")
    logger.info(f"  - Median location: Observation {cp_results['tau_median']}")
    logger.info(f"  - 95% Credible Interval: [{cp_results['tau_lower_95']}, {cp_results['tau_upper_95']}]")
    
    if cp_results['change_point_date']:
        logger.info(f"  - Date: {cp_results['change_point_date']}")
    
    logger.info(f"\nParameter Estimates:")
    logger.info(f"  - μ₁ (before): {param_results['mu1_mean']:.4f} (95% CI: [{param_results['mu1_lower_95']:.4f}, {param_results['mu1_upper_95']:.4f}])")
    logger.info(f"  - μ₂ (after): {param_results['mu2_mean']:.4f} (95% CI: [{param_results['mu2_lower_95']:.4f}, {param_results['mu2_upper_95']:.4f}])")
    logger.info(f"  - σ: {param_results['sigma_mean']:.4f} (95% CI: [{param_results['sigma_lower_95']:.4f}, {param_results['sigma_upper_95']:.4f}])")
    
    logger.info(f"\nImpact Quantification:")
    logger.info(f"  - Mean change: {param_results['impact_mean']:.4f}")
    logger.info(f"  - Percentage change: {param_results['impact_percent']:.2f}%")
    logger.info(f"  - 95% Credible Interval: [{param_results['impact_lower_95']:.4f}, {param_results['impact_upper_95']:.4f}]")
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ Bayesian Change Point Model completed successfully!")
    logger.info("=" * 80)
    
    return {
        'model': model,
        'cp_model': cp_model,
        'trace': trace,
        'convergence': convergence,
        'cp_results': cp_results,
        'param_results': param_results
    }


if __name__ == "__main__":
    results = main()
