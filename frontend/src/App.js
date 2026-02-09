import React, { useState, useEffect } from 'react';
import './App.css';
import api from './services/api';
import PriceChart from './components/PriceChart';
import EventHighlights from './components/EventHighlights';
import ChangePointDisplay from './components/ChangePointDisplay';
import Filters from './components/Filters';
import LoadingSpinner from './components/LoadingSpinner';
import EmptyState from './components/EmptyState';
import ErrorBoundary from './components/ErrorBoundary';

function App() {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [eventType, setEventType] = useState(null);
  const [impactLevel, setImpactLevel] = useState(null);
  
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);

  // Get unique event types
  const eventTypes = [...new Set(events.map(e => e.Event_Type))].sort();

  useEffect(() => {
    loadAllData();
  }, [startDate, endDate, eventType, impactLevel]);

  const loadAllData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load all data in parallel
      const [eventsResponse, changePointsResponse, summaryResponse] = await Promise.all([
        api.getEvents(startDate, endDate, eventType, impactLevel),
        api.getChangePoints(),
        api.getSummary()
      ]);

      setEvents(eventsResponse.events || []);
      setChangePoints(changePointsResponse.change_points || []);
      setSummary(summaryResponse);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleResetFilters = () => {
    setStartDate(null);
    setEndDate(null);
    setEventType(null);
    setImpactLevel(null);
    setSelectedEvent(null);
  };

  if (loading && !events.length) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Brent Oil Change Point Analysis Dashboard</h1>
          <p>Interactive visualization of oil prices, events, and change points</p>
        </header>
        <main style={{ padding: '20px', maxWidth: '1400px', margin: '0 auto' }}>
          <LoadingSpinner message="Loading dashboard data..." />
        </main>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="App">
        <header className="App-header">
          <h1>Brent Oil Change Point Analysis Dashboard</h1>
          <p>Interactive visualization of oil prices, events, and change points</p>
        </header>

        <main style={{ padding: '20px', maxWidth: '1400px', margin: '0 auto' }}>
        {error && (
          <div style={{
            backgroundColor: '#ffebee',
            color: '#c62828',
            padding: '15px',
            borderRadius: '4px',
            marginBottom: '20px'
          }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Filters */}
        <Filters
          startDate={startDate}
          endDate={endDate}
          eventType={eventType}
          impactLevel={impactLevel}
          onStartDateChange={setStartDate}
          onEndDateChange={setEndDate}
          onEventTypeChange={setEventType}
          onImpactLevelChange={setImpactLevel}
          eventTypes={eventTypes}
          onReset={handleResetFilters}
        />

        {/* Summary Statistics */}
        {summary && summary.summary_statistics && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '15px',
            marginBottom: '20px'
          }}>
            <div style={{
              backgroundColor: '#e3f2fd',
              padding: '15px',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <h4 style={{ margin: '0 0 10px 0' }}>Mean Price</h4>
              <p style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>
                ${summary.summary_statistics.mean?.toFixed(2) || 'N/A'}
              </p>
            </div>
            <div style={{
              backgroundColor: '#f3e5f5',
              padding: '15px',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <h4 style={{ margin: '0 0 10px 0' }}>Std Deviation</h4>
              <p style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>
                ${summary.summary_statistics.std?.toFixed(2) || 'N/A'}
              </p>
            </div>
            <div style={{
              backgroundColor: '#e8f5e9',
              padding: '15px',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <h4 style={{ margin: '0 0 10px 0' }}>Total Events</h4>
              <p style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>
                {events.length}
              </p>
            </div>
            <div style={{
              backgroundColor: '#fff3e0',
              padding: '15px',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <h4 style={{ margin: '0 0 10px 0' }}>Change Points</h4>
              <p style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>
                {changePoints.length}
              </p>
            </div>
          </div>
        )}

        {/* Price Chart */}
        <PriceChart
          startDate={startDate}
          endDate={endDate}
          highlightEvents={true}
        />

        {/* Change Point Display */}
        {changePoints.length > 0 && (
          <ChangePointDisplay changePoints={changePoints} />
        )}

        {/* Event Highlights */}
        {events.length > 0 ? (
          <EventHighlights 
            events={events} 
            changePoints={changePoints}
          />
        ) : (
          !loading && <EmptyState message="No events found for the selected filters" icon="📅" />
        )}

        {/* Events List (Drill-down) */}
        <div style={{ marginTop: '30px' }}>
          <h3>Events List</h3>
          {events.length > 0 ? (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
              gap: '15px'
            }}>
              {events.map((event, index) => (
              <div
                key={index}
                onClick={() => setSelectedEvent(selectedEvent === index ? null : index)}
                style={{
                  backgroundColor: selectedEvent === index ? '#e3f2fd' : 'white',
                  padding: '15px',
                  borderRadius: '8px',
                  border: '1px solid #ddd',
                  cursor: 'pointer',
                  transition: 'all 0.3s'
                }}
              >
                <h4 style={{ margin: '0 0 10px 0', color: '#2E86AB' }}>
                  {event.Event_Type}
                </h4>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>
                  <strong>Date:</strong> {new Date(event.Event_Date).toLocaleDateString()}
                </p>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>
                  <strong>Region:</strong> {event.Region}
                </p>
                <p style={{ margin: '5px 0', fontSize: '14px' }}>
                  <strong>Impact:</strong> 
                  <span style={{
                    color: event.Impact_Level === 'High' ? '#BC4749' : 
                           event.Impact_Level === 'Medium' ? '#F18F01' : '#6A994E',
                    fontWeight: 'bold',
                    marginLeft: '5px'
                  }}>
                    {event.Impact_Level}
                  </span>
                </p>
                {selectedEvent === index && (
                  <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #ddd' }}>
                    <p style={{ margin: '5px 0', fontSize: '13px' }}>
                      {event.Event_Description}
                    </p>
                  </div>
                )}
              </div>
              ))}
            </div>
          ) : (
            !loading && <EmptyState message="No events to display" icon="📋" />
          )}
        </div>
        </main>

        <footer style={{
          backgroundColor: '#2E86AB',
          color: 'white',
          padding: '20px',
          textAlign: 'center',
          marginTop: '40px'
        }}>
          <p style={{ margin: 0 }}>
            Brent Oil Change Point Analysis Dashboard | Birhan Energies
          </p>
          <p style={{ margin: '10px 0 0 0', fontSize: '14px', opacity: 0.8 }}>
            Data-driven insights for energy market decision-making
          </p>
        </footer>
      </div>
    </ErrorBoundary>
  );
}

export default App;
