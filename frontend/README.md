# Brent Oil Dashboard - Frontend

Interactive React dashboard for visualizing Brent oil price analysis, change points, and event correlations.

## Features

- **Interactive Price Charts**: Time series visualization with event highlights
- **Event Correlation**: Visual representation of how events impact oil prices
- **Change Point Analysis**: Display of detected structural breaks with parameter estimates
- **Advanced Filtering**: Date range, event type, and impact level filters
- **Drill-down Capability**: Click events for detailed information
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Setup

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Configuration

The frontend is configured to connect to the Flask backend at `http://localhost:5000` by default. This is set via the proxy in `package.json`.

To change the API URL, create a `.env` file in the `frontend` directory:

```
REACT_APP_API_URL=http://localhost:5000/api
```

### Running the Application

```bash
# Start development server
npm start
```

The application will open at `http://localhost:3000`.

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` directory.

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── PriceChart.js          # Main price time series chart
│   │   ├── EventHighlights.js     # Event impact visualization
│   │   ├── ChangePointDisplay.js # Change point analysis display
│   │   └── Filters.js             # Filter controls
│   ├── services/
│   │   └── api.js                 # API service for backend communication
│   ├── App.js                     # Main application component
│   ├── App.css                    # Application styles
│   └── index.js                   # Application entry point
├── package.json
└── README.md
```

## Components

### PriceChart
Displays the historical Brent oil price time series with:
- Interactive tooltips
- Event markers (vertical lines)
- Date range filtering support

### EventHighlights
Shows events and their impact on prices:
- Bar chart of event impacts
- Color-coded by impact level (High/Medium/Low)
- Detailed tooltips with event information

### ChangePointDisplay
Presents change point analysis results:
- Change point date and observation
- Parameter comparison (before/after)
- Price comparison visualization
- Impact statements

### Filters
Provides filtering controls:
- Date range selectors (start/end)
- Event type dropdown
- Impact level filter
- Reset button

## API Integration

The frontend communicates with the Flask backend through the `api.js` service:

- `GET /api/prices` - Historical price data
- `GET /api/change-points` - Change point results
- `GET /api/events` - Event correlation data
- `GET /api/summary` - Summary statistics
- `GET /api/stats` - Model performance metrics

## Responsive Design

The dashboard is fully responsive:
- **Desktop**: Full-width layout with side-by-side charts
- **Tablet**: Adjusted grid layouts, stacked components
- **Mobile**: Single column layout, optimized touch targets

## Technologies

- **React 18**: UI framework
- **Recharts**: Charting library for visualizations
- **CSS3**: Styling with responsive design

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure the Flask backend has CORS enabled and is running on the expected port.

### API Connection Errors
Check that:
1. The Flask backend is running (`python backend/app.py`)
2. The API URL in `.env` matches the backend URL
3. No firewall is blocking the connection

### Build Errors
If `npm run build` fails:
1. Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
2. Check for version conflicts in `package.json`
3. Ensure Node.js version is compatible (v14+)

## Development

### Adding New Components

1. Create component file in `src/components/`
2. Import and use in `App.js`
3. Add any required API calls to `api.js`

### Styling

Styles are defined in:
- `App.css` for global styles
- Inline styles in components for component-specific styling

Consider migrating to CSS Modules or styled-components for larger projects.

## License

Part of the Brent Oil Change Point Analysis project.
