#!/usr/bin/env python3
"""
Runner script for Task 1 analysis.

This script executes the comprehensive Task 1 foundation analysis,
including data loading, preprocessing, statistical analysis, and visualization.
"""

import sys
from pathlib import Path

# Add src and notebooks to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "notebooks"))

# Import using importlib to handle the filename with numbers
import importlib.util
spec = importlib.util.spec_from_file_location(
    "task1_analysis",
    project_root / "notebooks" / "01_task1_foundation_analysis.py"
)
task1_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task1_module)
main = task1_module.main

if __name__ == "__main__":
    try:
        results = main()
        print("\n✅ Task 1 analysis completed successfully!")
        print(f"📊 Analyzed {len(results['data'])} data points")
        print(f"📈 Detected {len(results['events'])} key events")
        print("📁 Results saved to reports/ directory")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        sys.exit(1)
