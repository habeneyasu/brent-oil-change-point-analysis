/**
 * API service for communicating with Flask backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class ApiService {
  /**
   * Fetch data from API endpoint
   */
  async fetchData(endpoint, params = {}) {
    try {
      const queryString = new URLSearchParams(params).toString();
      const url = `${API_BASE_URL}${endpoint}${queryString ? `?${queryString}` : ''}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      throw error;
    }
  }

  /**
   * Get historical price data
   */
  async getPrices(startDate = null, endDate = null) {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    return this.fetchData('/prices', params);
  }

  /**
   * Get change point results
   */
  async getChangePoints() {
    return this.fetchData('/change-points');
  }

  /**
   * Get events data
   */
  async getEvents(startDate = null, endDate = null, eventType = null, impactLevel = null) {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    if (eventType) params.event_type = eventType;
    if (impactLevel) params.impact_level = impactLevel;
    return this.fetchData('/events', params);
  }

  /**
   * Get summary statistics
   */
  async getSummary() {
    return this.fetchData('/summary');
  }

  /**
   * Get model statistics
   */
  async getStats() {
    return this.fetchData('/stats');
  }

  /**
   * Health check
   */
  async healthCheck() {
    return this.fetchData('/health');
  }
}

export default new ApiService();
