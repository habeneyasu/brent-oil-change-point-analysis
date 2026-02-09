/**
 * Price Chart Component
 * 
 * Interactive time series chart showing Brent oil prices with event highlights
 */

import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import api from '../services/api';

const PriceChart = ({ startDate, endDate, highlightEvents = true }) => {
  const [priceData, setPriceData] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [startDate, endDate]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load prices and events in parallel
      const [pricesResponse, eventsResponse] = await Promise.all([
        api.getPrices(startDate, endDate),
        api.getEvents(startDate, endDate)
      ]);

      // Format price data for chart
      const formattedPrices = pricesResponse.data.map(item => ({
        date: new Date(item.Date).toLocaleDateString(),
        price: parseFloat(item.Price),
        timestamp: new Date(item.Date)
      }));

      setPriceData(formattedPrices);
      setEvents(eventsResponse.events || []);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // Format tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{
          backgroundColor: 'white',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '4px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <p style={{ margin: 0, fontWeight: 'bold' }}>{data.date}</p>
          <p style={{ margin: '5px 0', color: '#2E86AB' }}>
            Price: ${data.price.toFixed(2)}
          </p>
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', minHeight: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid #f3f3f3',
            borderTop: '4px solid #2E86AB',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 10px'
          }}></div>
          <p>Loading price data...</p>
          <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px', color: 'red' }}>
        <p>Error loading data: {error}</p>
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: '400px', marginTop: '20px' }}>
      <h3 style={{ marginBottom: '10px' }}>Brent Oil Price Time Series</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={priceData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            angle={-45}
            textAnchor="end"
            height={80}
            interval="preserveStartEnd"
          />
          <YAxis
            label={{ value: 'Price (USD/barrel)', angle: -90, position: 'insideLeft' }}
            domain={['auto', 'auto']}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#2E86AB"
            strokeWidth={2}
            dot={false}
            name="Brent Oil Price"
          />
          {/* Add event markers */}
          {highlightEvents && events.map((event, index) => {
            const eventDate = new Date(event.Event_Date);
            const priceAtEvent = priceData.find(
              p => Math.abs(p.timestamp - eventDate) < 86400000 // Within 1 day
            );
            if (priceAtEvent) {
              return (
                <ReferenceLine
                  key={index}
                  x={priceAtEvent.date}
                  stroke="#F18F01"
                  strokeDasharray="5 5"
                  label={{
                    value: event.Event_Type.substring(0, 20),
                    position: 'top',
                    fill: '#F18F01',
                    fontSize: 10
                  }}
                />
              );
            }
            return null;
          })}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;
