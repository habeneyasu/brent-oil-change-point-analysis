# Unit Tests

This directory contains unit tests for the Brent oil change point analysis project.

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run with coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_data_loading.py
```

### Run with verbose output
```bash
pytest tests/ -v
```

## Test Structure

- `test_data_loading.py`: Tests for data loading and preprocessing
- `test_preprocessing.py`: Tests for time series analysis functions

## Test Coverage

Tests cover:
- Data loading with error handling
- Date parsing (multiple formats)
- Returns computation
- Trend analysis
- Stationarity testing
- Volatility analysis
- Summary statistics
