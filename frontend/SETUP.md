# Frontend Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

### 3. Ensure Backend is Running

Make sure the Flask backend is running on `http://localhost:5000`:

```bash
cd ../backend
python app.py
```

## Environment Configuration

Create a `.env` file in the `frontend` directory (optional):

```
REACT_APP_API_URL=http://localhost:5000/api
```

If not set, the app defaults to `http://localhost:5000/api` (configured via proxy in `package.json`).

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/
│   │   ├── PriceChart.js          # Main price visualization
│   │   ├── EventHighlights.js     # Event impact chart
│   │   ├── ChangePointDisplay.js  # Change point analysis
│   │   ├── Filters.js             # Filter controls
│   │   ├── LoadingSpinner.js      # Loading indicator
│   │   ├── EmptyState.js          # Empty state display
│   │   └── ErrorBoundary.js       # Error handling
│   ├── services/
│   │   └── api.js                 # API service layer
│   ├── App.js                     # Main application
│   ├── App.css                    # Application styles
│   ├── index.js                   # Entry point
│   └── index.css                  # Global styles
├── package.json
├── README.md
└── SETUP.md
```

## Features

✅ **Interactive Price Charts** - Time series with event markers  
✅ **Event Correlation** - Visual impact analysis  
✅ **Change Point Display** - Bayesian model results  
✅ **Advanced Filtering** - Date range, event type, impact level  
✅ **Drill-down** - Click events for details  
✅ **Responsive Design** - Mobile, tablet, desktop  
✅ **Error Handling** - Error boundaries and graceful failures  
✅ **Loading States** - User-friendly loading indicators  

## Troubleshooting

### Port Already in Use

If port 3000 is in use, React will prompt to use another port.

### CORS Errors

Ensure the Flask backend has CORS enabled and is running.

### API Connection Failed

1. Check backend is running: `curl http://localhost:5000/api/health`
2. Verify API URL in `.env` or `package.json` proxy setting
3. Check browser console for detailed error messages

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Development Tips

- Use React DevTools browser extension for debugging
- Check browser console for API errors
- Network tab shows all API requests
- Hot reload is enabled in development mode

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Next Steps

1. Customize styling in `App.css`
2. Add new components in `src/components/`
3. Extend API service in `src/services/api.js`
4. Add tests using React Testing Library
