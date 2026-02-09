/**
 * Event Highlights Component
 * 
 * Displays events with their impact on oil prices
 */

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';

const EventHighlights = ({ events, changePoints }) => {
  // Combine events with change point data
  const eventData = events.map(event => {
    // Find associated change point if any
    const associatedCP = changePoints.find(cp => {
      if (!cp.closest_event_date) return false;
      const cpDate = new Date(cp.closest_event_date);
      const eventDate = new Date(event.Event_Date);
      const daysDiff = Math.abs((cpDate - eventDate) / (1000 * 60 * 60 * 24));
      return daysDiff <= 90;
    });

    return {
      event: event.Event_Type.substring(0, 30),
      date: new Date(event.Event_Date).toLocaleDateString(),
      impact: associatedCP ? (associatedCP.impact_percent || 0) : 0,
      impactLevel: event.Impact_Level,
      region: event.Region
    };
  });

  // Color based on impact level
  const getColor = (impactLevel) => {
    switch (impactLevel) {
      case 'High': return '#BC4749';
      case 'Medium': return '#F18F01';
      default: return '#6A994E';
    }
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{
          backgroundColor: 'white',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '4px'
        }}>
          <p style={{ margin: 0, fontWeight: 'bold' }}>{data.event}</p>
          <p style={{ margin: '5px 0' }}>Date: {data.date}</p>
          <p style={{ margin: '5px 0' }}>Region: {data.region}</p>
          <p style={{ margin: '5px 0' }}>Impact Level: {data.impactLevel}</p>
          {data.impact !== 0 && (
            <p style={{ margin: '5px 0', color: data.impact > 0 ? 'green' : 'red' }}>
              Price Impact: {data.impact > 0 ? '+' : ''}{data.impact.toFixed(2)}%
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ width: '100%', height: '400px', marginTop: '20px' }}>
      <h3>Events and Price Impact</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={eventData} margin={{ top: 5, right: 30, left: 20, bottom: 100 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="event"
            angle={-45}
            textAnchor="end"
            height={120}
            interval={0}
          />
          <YAxis label={{ value: 'Impact (%)', angle: -90, position: 'insideLeft' }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar dataKey="impact" name="Price Impact">
            {eventData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.impactLevel)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EventHighlights;
