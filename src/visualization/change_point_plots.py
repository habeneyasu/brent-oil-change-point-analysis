"""
Visualization module for change point analysis results.

This module provides functions for visualizing Bayesian change point
model outputs including trace plots, posterior distributions, and
convergence diagnostics.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import arviz as az
from pathlib import Path
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class ChangePointVisualizer:
    """
    Class for visualizing change point model results.
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
    
    def plot_trace(
        self,
        trace: az.InferenceData,
        var_names: Optional[list] = None,
        title: str = "MCMC Trace Plots",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """
        Plot MCMC trace plots for convergence diagnostics.
        
        Args:
            trace: ArviZ InferenceData object
            var_names: List of variable names to plot. If None, plots all.
            title: Plot title
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        try:
            # Get available variables from trace
            available_vars = list(trace.posterior.data_vars.keys())
            
            # Handle prefixed variable names (e.g., "model_name::tau")
            def find_vars(requested_names):
                """Find variables with or without prefix."""
                found_vars = []
                for req_name in requested_names:
                    for var in available_vars:
                        if var.endswith(f"::{req_name}") or var == req_name:
                            found_vars.append(var)
                            break
                return found_vars
            
            # If var_names not specified, use all available
            if var_names is None:
                var_names_for_plot = available_vars
            else:
                # Find actual variable names (with prefix if present)
                var_names_for_plot = find_vars(var_names)
                if not var_names_for_plot:
                    # If none found, use all available
                    var_names_for_plot = available_vars
                    self.logger.warning(
                        f"Requested variables {var_names} not found. "
                        f"Using available variables: {var_names_for_plot}"
                    )
            
            # Use ArviZ plot_trace with actual variable names
            axes = az.plot_trace(
                trace,
                var_names=var_names_for_plot if var_names_for_plot else None,
                compact=True,
                divergences="bottom"
            )
            
            # Get figure from axes
            if hasattr(axes, 'flat'):
                fig = axes.flat[0].figure
            elif hasattr(axes, 'figure'):
                fig = axes.figure
            elif isinstance(axes, np.ndarray):
                fig = axes.flat[0].figure if len(axes.flat) > 0 else plt.gcf()
            else:
                fig = plt.gcf()
            
            fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
            
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "trace_plots.png"
            else:
                save_path = Path(save_path)
            
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved trace plots to {save_path}")
            
            return fig
            
        except Exception as e:
            error_msg = f"Error plotting trace: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise
    
    def plot_tau_posterior(
        self,
        tau_samples: np.ndarray,
        title: str = "Posterior Distribution of Change Point (τ)",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """
        Plot posterior distribution of change point tau.
        A sharp, narrow peak indicates high certainty.
        
        Args:
            tau_samples: Array of tau samples from posterior
            title: Plot title
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            # Histogram
            ax1.hist(
                tau_samples,
                bins=50,
                color='#2E86AB',
                alpha=0.7,
                edgecolor='black',
                density=True
            )
            ax1.axvline(
                np.median(tau_samples),
                color='red',
                linestyle='--',
                linewidth=2,
                label=f'Median: {int(np.median(tau_samples))}'
            )
            ax1.axvline(
                np.mean(tau_samples),
                color='orange',
                linestyle='--',
                linewidth=2,
                label=f'Mean: {int(np.mean(tau_samples))}'
            )
            ax1.set_xlabel('Change Point Location (τ)', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Density', fontsize=12, fontweight='bold')
            ax1.set_title('Posterior Distribution - Histogram', fontsize=12, fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # KDE plot
            from scipy import stats
            kde = stats.gaussian_kde(tau_samples)
            x_range = np.linspace(tau_samples.min(), tau_samples.max(), 200)
            ax2.plot(x_range, kde(x_range), linewidth=2, color='#A23B72')
            ax2.fill_between(x_range, kde(x_range), alpha=0.3, color='#A23B72')
            ax2.axvline(
                np.median(tau_samples),
                color='red',
                linestyle='--',
                linewidth=2,
                label=f'Median: {int(np.median(tau_samples))}'
            )
            
            # Add 95% credible interval
            hdi = az.hdi(tau_samples, hdi_prob=0.95)
            ax2.axvspan(hdi[0], hdi[1], alpha=0.2, color='yellow', label='95% HDI')
            
            ax2.set_xlabel('Change Point Location (τ)', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Density', fontsize=12, fontweight='bold')
            ax2.set_title('Posterior Distribution - KDE', fontsize=12, fontweight='bold')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "tau_posterior.png"
            else:
                save_path = Path(save_path)
            
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved tau posterior plot to {save_path}")
            
            return fig
            
        except Exception as e:
            error_msg = f"Error plotting tau posterior: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise
    
    def plot_parameter_posteriors(
        self,
        mu1_samples: np.ndarray,
        mu2_samples: np.ndarray,
        sigma_samples: np.ndarray,
        title: str = "Posterior Distributions of Model Parameters",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """
        Plot posterior distributions for before/after parameters.
        
        Args:
            mu1_samples: Samples of mu1 (before change point)
            mu2_samples: Samples of mu2 (after change point)
            sigma_samples: Samples of sigma (standard deviation)
            title: Plot title
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        try:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            
            # Mu1 (before)
            ax = axes[0, 0]
            ax.hist(mu1_samples, bins=50, color='#6A994E', alpha=0.7, edgecolor='black', density=True)
            ax.axvline(np.mean(mu1_samples), color='red', linestyle='--', linewidth=2,
                      label=f'Mean: {np.mean(mu1_samples):.4f}')
            hdi = az.hdi(mu1_samples, hdi_prob=0.95)
            ax.axvspan(hdi[0], hdi[1], alpha=0.2, color='yellow', label='95% HDI')
            ax.set_xlabel('μ₁ (Before Change Point)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Density', fontsize=12, fontweight='bold')
            ax.set_title('Posterior: μ₁ (Mean Before)', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Mu2 (after)
            ax = axes[0, 1]
            ax.hist(mu2_samples, bins=50, color='#F18F01', alpha=0.7, edgecolor='black', density=True)
            ax.axvline(np.mean(mu2_samples), color='red', linestyle='--', linewidth=2,
                      label=f'Mean: {np.mean(mu2_samples):.4f}')
            hdi = az.hdi(mu2_samples, hdi_prob=0.95)
            ax.axvspan(hdi[0], hdi[1], alpha=0.2, color='yellow', label='95% HDI')
            ax.set_xlabel('μ₂ (After Change Point)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Density', fontsize=12, fontweight='bold')
            ax.set_title('Posterior: μ₂ (Mean After)', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Impact (mu2 - mu1)
            ax = axes[1, 0]
            impact_samples = mu2_samples - mu1_samples
            ax.hist(impact_samples, bins=50, color='#A23B72', alpha=0.7, edgecolor='black', density=True)
            ax.axvline(np.mean(impact_samples), color='red', linestyle='--', linewidth=2,
                      label=f'Mean: {np.mean(impact_samples):.4f}')
            ax.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
            hdi = az.hdi(impact_samples, hdi_prob=0.95)
            ax.axvspan(hdi[0], hdi[1], alpha=0.2, color='yellow', label='95% HDI')
            ax.set_xlabel('Impact (μ₂ - μ₁)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Density', fontsize=12, fontweight='bold')
            ax.set_title('Posterior: Impact (Change in Mean)', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Sigma
            ax = axes[1, 1]
            ax.hist(sigma_samples, bins=50, color='#BC4749', alpha=0.7, edgecolor='black', density=True)
            ax.axvline(np.mean(sigma_samples), color='red', linestyle='--', linewidth=2,
                      label=f'Mean: {np.mean(sigma_samples):.4f}')
            hdi = az.hdi(sigma_samples, hdi_prob=0.95)
            ax.axvspan(hdi[0], hdi[1], alpha=0.2, color='yellow', label='95% HDI')
            ax.set_xlabel('σ (Standard Deviation)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Density', fontsize=12, fontweight='bold')
            ax.set_title('Posterior: σ (Volatility)', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            plt.suptitle(title, fontsize=14, fontweight='bold', y=0.995)
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "parameter_posteriors.png"
            else:
                save_path = Path(save_path)
            
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Saved parameter posteriors plot to {save_path}")
            
            return fig
            
        except Exception as e:
            error_msg = f"Error plotting parameter posteriors: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise
