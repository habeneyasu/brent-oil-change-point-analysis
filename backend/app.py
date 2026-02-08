"""
Flask application for serving Brent oil price analysis API
"""

from flask import Flask
from flask_cors import CORS
from config import config

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
        return {'message': 'Brent Oil Change Point Analysis API', 'status': 'running'}
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, port=5000)
