/**
 * Empty State Component
 * 
 * Displays when no data is available
 */

import React from 'react';

const EmptyState = ({ message = 'No data available', icon = '📊' }) => {
  return (
    <div style={{
      padding: '60px 20px',
      textAlign: 'center',
      color: '#666'
    }}>
      <div style={{ fontSize: '64px', marginBottom: '20px' }}>{icon}</div>
      <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>No Data</h3>
      <p style={{ margin: 0, fontSize: '16px' }}>{message}</p>
    </div>
  );
};

export default EmptyState;
