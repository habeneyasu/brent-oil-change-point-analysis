"""
API routes for serving analysis data.

This module provides Flask API endpoints for:
- Historical price data
- Change point results
- Event correlation data
- Summary statistics and metrics
"""

from flask import Blueprint, jsonify, request
from api.data_service import DataService, DataServiceError
import logging

logger = logging.getLogger(__name__)

# Initialize data service
data_service = DataService()

api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Brent Oil Change Point Analysis API',
        'version': '1.0.0'
    })


@api_bp.route('/prices', methods=['GET'])
def get_prices():
    """
    Get historical price data.
    
    Query Parameters:
        start_date (optional): Start date filter (YYYY-MM-DD)
        end_date (optional): End date filter (YYYY-MM-DD)
    
    Returns:
        JSON with price data, count, and statistics
    """
    try:
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        
        logger.info(f"Requesting price data: start={start_date}, end={end_date}")
        
        result = data_service.get_historical_prices(
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify(result), 200
        
    except DataServiceError as e:
        logger.error(f"Data service error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/change-points', methods=['GET'])
def get_change_points():
    """
    Get detected change points from analysis.
    
    Returns:
        JSON with change point data including:
        - Change point date and location
        - Parameter estimates (mu1, mu2, sigma)
        - Impact quantification
        - Associated events
    """
    try:
        logger.info("Requesting change point data")
        
        result = data_service.get_change_points()
        
        return jsonify(result), 200
        
    except DataServiceError as e:
        logger.error(f"Data service error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/events', methods=['GET'])
def get_events():
    """
    Get event correlation data.
    
    Query Parameters:
        start_date (optional): Start date filter (YYYY-MM-DD)
        end_date (optional): End date filter (YYYY-MM-DD)
        event_type (optional): Filter by event type
        impact_level (optional): Filter by impact level (High, Medium, Low)
    
    Returns:
        JSON with event data and filters applied
    """
    try:
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        event_type = request.args.get('event_type', None)
        impact_level = request.args.get('impact_level', None)
        
        logger.info(
            f"Requesting events: start={start_date}, end={end_date}, "
            f"type={event_type}, impact={impact_level}"
        )
        
        result = data_service.get_events(
            start_date=start_date,
            end_date=end_date,
            event_type=event_type,
            impact_level=impact_level
        )
        
        return jsonify(result), 200
        
    except DataServiceError as e:
        logger.error(f"Data service error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Get summary statistics and analysis metrics.
    
    Returns:
        JSON with summary statistics, volatility analysis, and key metrics
    """
    try:
        logger.info("Requesting summary statistics")
        
        summary_stats = data_service.get_summary_statistics()
        volatility = data_service.get_volatility_analysis()
        
        result = {
            'summary_statistics': summary_stats,
            'volatility_analysis': volatility
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get performance metrics and model statistics.
    
    Returns:
        JSON with model performance metrics
    """
    try:
        logger.info("Requesting model statistics")
        
        # Load stationarity tests if available
        stats_file = data_service.reports_dir / "stationarity_tests.csv"
        stationarity = {}
        
        if stats_file.exists():
            import pandas as pd
            stationarity_data = pd.read_csv(stats_file)
            stationarity = stationarity_data.to_dict('records')
        
        result = {
            'stationarity_tests': stationarity,
            'data_availability': {
                'prices': data_service._price_data_cache is not None,
                'events': data_service._events_cache is not None,
                'change_points': data_service.get_change_points()['count'] > 0
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
