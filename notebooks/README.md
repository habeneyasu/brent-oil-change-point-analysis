# Notebooks Directory

This directory contains analysis scripts and notebooks for the Brent oil change point analysis project.

## Current Structure

### Task 1 Files
- **`01_task1_foundation_analysis.py`**: Python script for automated execution
- **`01_task1_foundation_analysis.ipynb`**: Jupyter notebook for interactive exploration

**Note**: Both files serve different purposes:
- `.py` script: Best for automation, CI/CD, and reproducible runs
- `.ipynb` notebook: Best for interactive exploration, visualization, and learning

### Task 2 Files
- **`02_task2_change_point_analysis.py`**: Core analysis - data preparation and EDA
- **`02b_build_change_point_model.py`**: Build and run Bayesian change point model

**Note**: Currently Python scripts only. Can add `.ipynb` versions for interactive exploration if needed.

## Usage

### Running Python Scripts
```bash
# From project root
python notebooks/01_task1_foundation_analysis.py
python notebooks/02_task2_change_point_analysis.py
python notebooks/02b_build_change_point_model.py
```

### Running Jupyter Notebooks
```bash
# Start Jupyter
jupyter notebook notebooks/01_task1_foundation_analysis.ipynb

# Or JupyterLab
jupyter lab notebooks/01_task1_foundation_analysis.ipynb
```

## Best Practices

1. **Python Scripts (.py)**: 
   - Use for automation and reproducibility
   - Better for version control (easier to diff)
   - Suitable for CI/CD pipelines
   - Run from command line

2. **Jupyter Notebooks (.ipynb)**:
   - Use for interactive exploration
   - Better for visualization and step-by-step analysis
   - Good for documentation and teaching
   - Run in Jupyter environment

3. **Avoid Duplication**:
   - If both exist, they should serve different purposes
   - Notebooks can import from `.py` scripts to avoid code duplication
   - Or use notebooks as interactive wrappers around script functions

## Recommendations

- ✅ **Current structure is acceptable**: Task 1 has both formats serving different purposes
- ✅ **Task 2 scripts are fine**: Python scripts work well for automation
- 💡 **Optional**: Create `.ipynb` for Task 2 if interactive exploration is needed

## Output

All scripts and notebooks:
- Save visualizations to `reports/` directory
- Save analysis results (CSV) to `reports/` directory
- Use modules from `src/` directory
- Follow consistent logging and error handling patterns
