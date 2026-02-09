"""
Bayesian Change Point Model for Brent Oil Price Analysis.

This module implements Bayesian change point detection using PyMC
to identify structural breaks in time series data.
"""

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
from typing import Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ChangePointModelError(Exception):
    """Custom exception for change point model errors."""
    pass


class BayesianChangePointModel:
    """
    Bayesian change point detection model using PyMC.
    
    Implements a simple change point model that detects shifts
    in the mean of a time series.
    """
    
    def __init__(self, data: pd.Series, model_name: str = "change_point_model"):
        """
        Initialize the change point model.
        
        Args:
            data: Time series data (prices or returns)
            model_name: Name for the PyMC model
        """
        if len(data) < 10:
            raise ChangePointModelError(
                "Data must contain at least 10 observations"
            )
        
        self.data = data.values
        self.data_index = data.index if hasattr(data, 'index') else None
        self.n_obs = len(data)
        self.model_name = model_name
        self.model: Optional[pm.Model] = None
        self.trace: Optional[az.InferenceData] = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
    def build_model(self) -> pm.Model:
        """
        Build the Bayesian change point model.
        
        Model structure:
        - tau: Change point location (discrete uniform prior)
        - mu1, mu2: Mean before and after change point
        - sigma: Standard deviation (assumed constant)
        
        Returns:
            PyMC model
        """
        try:
            self.logger.info(f"Building change point model for {self.n_obs} observations")
            
            with pm.Model(name=self.model_name) as model:
                # Prior for change point location
                # Uniform over all possible days (excluding first and last)
                tau = pm.DiscreteUniform(
                    "tau",
                    lower=1,
                    upper=self.n_obs - 1,
                    initval=self.n_obs // 2
                )
                
                # Priors for means before and after change point
                mu1 = pm.Normal("mu1", mu=np.mean(self.data), sigma=np.std(self.data) * 2)
                mu2 = pm.Normal("mu2", mu=np.mean(self.data), sigma=np.std(self.data) * 2)
                
                # Prior for standard deviation
                sigma = pm.HalfNormal("sigma", sigma=np.std(self.data))
                
                # Switch function: use mu1 before tau, mu2 after tau
                mu = pm.math.switch(tau >= np.arange(self.n_obs), mu1, mu2)
                
                # Likelihood
                likelihood = pm.Normal(
                    "likelihood",
                    mu=mu,
                    sigma=sigma,
                    observed=self.data
                )
            
            self.model = model
            self.logger.info("Model built successfully")
            
            return model
            
        except Exception as e:
            error_msg = f"Error building model: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise ChangePointModelError(error_msg) from e
    
    def sample(
        self,
        draws: int = 2000,
        tune: int = 1000,
        chains: int = 4,
        target_accept: float = 0.95,
        random_seed: Optional[int] = None
    ) -> az.InferenceData:
        """
        Run MCMC sampling.
        
        Args:
            draws: Number of samples to draw
            tune: Number of tuning steps
            chains: Number of chains
            target_accept: Target acceptance rate
            random_seed: Random seed for reproducibility
            
        Returns:
            InferenceData object with trace
        """
        try:
            if self.model is None:
                raise ChangePointModelError(
                    "Model must be built before sampling. Call build_model() first."
                )
            
            self.logger.info(
                f"Starting MCMC sampling: {chains} chains, {draws} draws, {tune} tune steps"
            )
            
            with self.model:
                self.trace = pm.sample(
                    draws=draws,
                    tune=tune,
                    chains=chains,
                    target_accept=target_accept,
                    random_seed=random_seed,
                    return_inferencedata=True,
                    progressbar=True
                )
            
            self.logger.info("MCMC sampling completed successfully")
            
            return self.trace
            
        except Exception as e:
            error_msg = f"Error during sampling: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise ChangePointModelError(error_msg) from e
    
    def check_convergence(self) -> Dict:
        """
        Check MCMC convergence diagnostics.
        
        Returns:
            Dictionary with convergence metrics (R-hat, ESS, etc.)
        """
        try:
            if self.trace is None:
                raise ChangePointModelError(
                    "No trace available. Run sample() first."
                )
            
            # Get available variable names from trace
            available_vars = list(self.trace.posterior.data_vars.keys())
            self.logger.debug(f"Available variables in trace: {available_vars}")
            
            # Handle prefixed variable names (e.g., "model_name::tau")
            # Try to find variables with or without prefix
            def find_vars(requested_names):
                found_vars = []
                for req_name in requested_names:
                    for var in available_vars:
                        if var.endswith(f"::{req_name}") or var == req_name:
                            found_vars.append(var)
                            break
                return found_vars
            
            requested_vars = ["tau", "mu1", "mu2", "sigma"]
            var_names = find_vars(requested_vars)
            
            if not var_names:
                # If none of the requested vars are found, use all available
                var_names = available_vars
                self.logger.warning(
                    f"Requested variables {requested_vars} not found. "
                    f"Using available variables: {var_names}"
                )
            
            # Compute summary statistics
            summary = az.summary(self.trace, var_names=var_names if var_names else None)
            
            # Check R-hat (should be < 1.01 for convergence)
            if 'r_hat' in summary.columns:
                r_hat = summary['r_hat'].to_dict()
                converged = all(r < 1.01 for r in r_hat.values())
            else:
                r_hat = {}
                converged = None
                self.logger.warning("R-hat not available in summary")
            
            # Effective sample size
            ess = {}
            if 'ess_bulk' in summary.columns:
                ess = summary['ess_bulk'].to_dict()
            elif 'ess' in summary.columns:
                ess = summary['ess'].to_dict()
            
            convergence_results = {
                'converged': converged,
                'r_hat': r_hat,
                'ess_bulk': ess,
                'summary': summary,
                'available_vars': available_vars
            }
            
            if converged is True:
                self.logger.info("✅ Model converged (all R-hat < 1.01)")
            elif converged is False:
                self.logger.warning("⚠️ Model may not have converged (some R-hat >= 1.01)")
            else:
                self.logger.info("Convergence check completed (R-hat not available)")
            
            return convergence_results
            
        except Exception as e:
            error_msg = f"Error checking convergence: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise ChangePointModelError(error_msg) from e
    
    def get_change_point_posterior(self) -> Dict:
        """
        Extract posterior distribution of change point.
        
        Returns:
            Dictionary with change point statistics
        """
        try:
            if self.trace is None:
                raise ChangePointModelError(
                    "No trace available. Run sample() first."
                )
            
            # Check available variables
            available_vars = list(self.trace.posterior.data_vars.keys())
            
            # Handle prefixed variable names (e.g., "model_name::tau")
            tau_var = None
            for var in available_vars:
                if var.endswith("::tau") or var == "tau":
                    tau_var = var
                    break
            
            if tau_var is None:
                raise ChangePointModelError(
                    f"Variable 'tau' not found in trace. Available variables: {available_vars}"
                )
            
            # Extract tau samples
            tau_samples = self.trace.posterior[tau_var].values.flatten()
            
            # Compute statistics
            tau_mean = float(np.mean(tau_samples))
            tau_median = float(np.median(tau_samples))
            tau_std = float(np.std(tau_samples))
            
            # Credible intervals
            tau_hdi = az.hdi(tau_samples, hdi_prob=0.95)
            tau_lower = float(tau_hdi[0])
            tau_upper = float(tau_hdi[1])
            
            # Most probable change point (mode)
            tau_mode = int(pd.Series(tau_samples).mode()[0])
            
            # Convert to date if index is available
            change_point_date = None
            if self.data_index is not None:
                try:
                    change_point_date = self.data_index[int(tau_median)]
                except (IndexError, TypeError):
                    pass
            
            results = {
                'tau_mean': tau_mean,
                'tau_median': int(tau_median),
                'tau_mode': tau_mode,
                'tau_std': tau_std,
                'tau_lower_95': int(tau_lower),
                'tau_upper_95': int(tau_upper),
                'change_point_date': change_point_date,
                'tau_samples': tau_samples
            }
            
            self.logger.info(
                f"Change point detected at observation {tau_median} "
                f"(95% HDI: {tau_lower:.0f} - {tau_upper:.0f})"
            )
            
            return results
            
        except Exception as e:
            error_msg = f"Error extracting change point posterior: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise ChangePointModelError(error_msg) from e
    
    def get_parameter_posteriors(self) -> Dict:
        """
        Extract posterior distributions of model parameters.
        
        Returns:
            Dictionary with parameter statistics
        """
        try:
            if self.trace is None:
                raise ChangePointModelError(
                    "No trace available. Run sample() first."
                )
            
            # Check available variables
            available_vars = list(self.trace.posterior.data_vars.keys())
            
            # Handle prefixed variable names (e.g., "model_name::mu1")
            def find_var(name):
                for var in available_vars:
                    if var.endswith(f"::{name}") or var == name:
                        return var
                return None
            
            mu1_var = find_var("mu1")
            mu2_var = find_var("mu2")
            sigma_var = find_var("sigma")
            
            missing_vars = []
            if mu1_var is None:
                missing_vars.append("mu1")
            if mu2_var is None:
                missing_vars.append("mu2")
            if sigma_var is None:
                missing_vars.append("sigma")
            
            if missing_vars:
                raise ChangePointModelError(
                    f"Variables {missing_vars} not found in trace. "
                    f"Available variables: {available_vars}"
                )
            
            # Extract parameter samples
            mu1_samples = self.trace.posterior[mu1_var].values.flatten()
            mu2_samples = self.trace.posterior[mu2_var].values.flatten()
            sigma_samples = self.trace.posterior[sigma_var].values.flatten()
            
            # Compute statistics for each parameter
            def compute_stats(samples, name):
                return {
                    f'{name}_mean': float(np.mean(samples)),
                    f'{name}_median': float(np.median(samples)),
                    f'{name}_std': float(np.std(samples)),
                    f'{name}_lower_95': float(np.percentile(samples, 2.5)),
                    f'{name}_upper_95': float(np.percentile(samples, 97.5)),
                    f'{name}_samples': samples
                }
            
            results = {
                **compute_stats(mu1_samples, 'mu1'),
                **compute_stats(mu2_samples, 'mu2'),
                **compute_stats(sigma_samples, 'sigma')
            }
            
            # Compute impact (difference between means)
            impact_samples = mu2_samples - mu1_samples
            results.update({
                'impact_mean': float(np.mean(impact_samples)),
                'impact_median': float(np.median(impact_samples)),
                'impact_std': float(np.std(impact_samples)),
                'impact_lower_95': float(np.percentile(impact_samples, 2.5)),
                'impact_upper_95': float(np.percentile(impact_samples, 97.5)),
                'impact_percent': float((np.mean(impact_samples) / np.mean(mu1_samples)) * 100),
                'impact_samples': impact_samples
            })
            
            self.logger.info(
                f"Parameter estimates: μ₁={results['mu1_mean']:.2f}, "
                f"μ₂={results['mu2_mean']:.2f}, "
                f"Impact={results['impact_percent']:.1f}%"
            )
            
            return results
            
        except Exception as e:
            error_msg = f"Error extracting parameter posteriors: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise ChangePointModelError(error_msg) from e
