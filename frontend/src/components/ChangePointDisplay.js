/**
 * Change Point Display Component
 * 
 * Shows detected change points with parameter estimates and impact
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

const ChangePointDisplay = ({ changePoints }) => {
  if (!changePoints || changePoints.length === 0) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>No change points detected. Run Task 2 analysis first.</p>
      </div>
    );
  }

  const cp = changePoints[0];

  // Prepare data for visualization
  const parameterData = [
    {
      parameter: 'Before (μ₁)',
      value: parseFloat(cp.mu1) || 0,
      color: '#6A994E'
    },
    {
      parameter: 'After (μ₂)',
      value: parseFloat(cp.mu2) || 0,
      color: '#F18F01'
    },
    {
      parameter: 'Impact',
      value: parseFloat(cp.impact_percent) || 0,
      color: cp.impact_percent > 0 ? '#BC4749' : '#2E86AB'
    }
  ];

  const priceData = [
    {
      period: 'Before Change',
      price: parseFloat(cp.price_before) || 0
    },
    {
      period: 'After Change',
      price: parseFloat(cp.price_after) || 0
    }
  ];

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Change Point Analysis</h3>
      
      <div style={{ 
        backgroundColor: '#f5f5f5', 
        padding: '15px', 
        borderRadius: '8px',
        marginBottom: '20px'
      }}>
        <h4>Change Point Details</h4>
        <p><strong>Date:</strong> {cp.change_point_date ? new Date(cp.change_point_date).toLocaleDateString() : 'N/A'}</p>
        <p><strong>Observation:</strong> {cp.change_point_obs}</p>
        {cp.impact_statement && (
          <p><strong>Impact Statement:</strong> {cp.impact_statement}</p>
        )}
        {cp.closest_event && (
          <p><strong>Associated Event:</strong> {cp.closest_event}</p>
        )}
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
        {/* Parameter Comparison */}
        <div style={{ flex: '1', minWidth: '300px' }}>
          <h4>Parameter Comparison</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={parameterData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="parameter" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" name="Value">
                {parameterData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Price Comparison */}
        <div style={{ flex: '1', minWidth: '300px' }}>
          <h4>Average Price: Before vs After</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={priceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" />
              <YAxis label={{ value: 'Price (USD)', angle: -90 }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="price" fill="#2E86AB" name="Average Price" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default ChangePointDisplay;
