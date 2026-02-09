/**
 * Filters Component
 * 
 * Date range selectors and event filters
 */

import React from 'react';

const Filters = ({ 
  startDate, 
  endDate, 
  eventType, 
  impactLevel,
  onStartDateChange,
  onEndDateChange,
  onEventTypeChange,
  onImpactLevelChange,
  eventTypes,
  onReset
}) => {
  return (
    <div style={{
      backgroundColor: '#f9f9f9',
      padding: '20px',
      borderRadius: '8px',
      marginBottom: '20px',
      display: 'flex',
      flexWrap: 'wrap',
      gap: '15px',
      alignItems: 'flex-end'
    }}>
      <div style={{ flex: '1', minWidth: '200px' }}>
        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
          Start Date
        </label>
        <input
          type="date"
          value={startDate || ''}
          onChange={(e) => onStartDateChange(e.target.value)}
          style={{
            width: '100%',
            padding: '8px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
        />
      </div>

      <div style={{ flex: '1', minWidth: '200px' }}>
        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
          End Date
        </label>
        <input
          type="date"
          value={endDate || ''}
          onChange={(e) => onEndDateChange(e.target.value)}
          style={{
            width: '100%',
            padding: '8px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
        />
      </div>

      <div style={{ flex: '1', minWidth: '200px' }}>
        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
          Event Type
        </label>
        <select
          value={eventType || ''}
          onChange={(e) => onEventTypeChange(e.target.value || null)}
          style={{
            width: '100%',
            padding: '8px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
        >
          <option value="">All Types</option>
          {eventTypes.map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>

      <div style={{ flex: '1', minWidth: '200px' }}>
        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
          Impact Level
        </label>
        <select
          value={impactLevel || ''}
          onChange={(e) => onImpactLevelChange(e.target.value || null)}
          style={{
            width: '100%',
            padding: '8px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
        >
          <option value="">All Levels</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>

      <div>
        <button
          onClick={onReset}
          style={{
            padding: '8px 16px',
            backgroundColor: '#6A994E',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Reset Filters
        </button>
      </div>
    </div>
  );
};

export default Filters;
