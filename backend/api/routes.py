"""
API routes for serving analysis data
"""

from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

@api_bp.route('/prices', methods=['GET'])
def get_prices():
    """Get historical price data"""
    # TODO: Implement data loading from processed data
    return jsonify({'message': 'Endpoint under construction'})

@api_bp.route('/change-points', methods=['GET'])
def get_change_points():
    """Get detected change points"""
    # TODO: Implement change point data retrieval
    return jsonify({'message': 'Endpoint under construction'})

@api_bp.route('/events', methods=['GET'])
def get_events():
    """Get event data"""
    # TODO: Implement event data retrieval
    return jsonify({'message': 'Endpoint under construction'})
