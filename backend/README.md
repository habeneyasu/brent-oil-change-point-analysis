# Flask Backend API

RESTful API for serving Brent oil price analysis results to the dashboard frontend.

## API Endpoints

### Health Check
- **GET** `/api/health`
- Returns API status and version

### Historical Price Data
- **GET** `/api/prices`
- Query Parameters:
  - `start_date` (optional): Filter from date (YYYY-MM-DD)
  - `end_date` (optional): Filter to date (YYYY-MM-DD)
- Returns: Price data with statistics

### Change Point Results
- **GET** `/api/change-points`
- Returns: Detected change points with parameter estimates and impact quantification

### Event Correlation Data
- **GET** `/api/events`
- Query Parameters:
  - `start_date` (optional): Filter from date
  - `end_date` (optional): Filter to date
  - `event_type` (optional): Filter by event type
  - `impact_level` (optional): Filter by impact level (High, Medium, Low)
- Returns: Event data matching filters

### Summary Statistics
- **GET** `/api/summary`
- Returns: Summary statistics and volatility analysis

### Model Statistics
- **GET** `/api/stats`
- Returns: Model performance metrics and stationarity tests

## Setup

```bash
# From project root
cd backend

# Install dependencies (from root)
pip install -r ../requirements.txt
pip install -r requirements.txt

# Run the server
python app.py
```

The API will run on `http://localhost:5000`

## Usage Examples

```bash
# Get all prices
curl http://localhost:5000/api/prices

# Get prices for date range
curl "http://localhost:5000/api/prices?start_date=2020-01-01&end_date=2022-12-31"

# Get change points
curl http://localhost:5000/api/change-points

# Get events
curl http://localhost:5000/api/events

# Get high-impact events
curl "http://localhost:5000/api/events?impact_level=High"
```

## Data Sources

The API serves data from:
- `data/raw/BrentOilPrices.csv` - Historical prices
- `data/external/key_events.csv` - Event data
- `reports/*.csv` - Analysis results (change points, statistics)

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `404`: Endpoint not found
- `500`: Internal server error

Error responses include an `error` field with a descriptive message.
