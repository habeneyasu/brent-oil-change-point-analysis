"""
Flask application for serving Brent oil price analysis API
"""

from flask import Flask, jsonify
from flask_cors import CORS
from config import config
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        """Root endpoint with API information"""
        return jsonify({
            'message': 'Brent Oil Change Point Analysis API',
            'status': 'running',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'prices': '/api/prices',
                'change_points': '/api/change-points',
                'events': '/api/events',
                'summary': '/api/summary',
                'stats': '/api/stats'
            }
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    logger.info("Flask application initialized")
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, port=5000)
