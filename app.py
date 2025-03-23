import os
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
from recommendation_engine import TradingRecommendationEngine

app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Enable CORS for all routes

# Initialize recommendation engine
engine = TradingRecommendationEngine()

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """API endpoint to get trading recommendations"""
    timeframe = request.args.get('timeframe', '24h')
    if timeframe not in ['12h', '24h', '3d', '1w']:
        timeframe = '24h'  # Default to 24h if invalid timeframe
    
    # Get specific assets if provided
    assets = request.args.get('assets')
    if assets:
        assets = assets.split(',')
    
    # Generate recommendations
    recommendations = engine.get_recommendations(timeframe, assets)
    return jsonify(recommendations)

@app.route('/api/assets', methods=['GET'])
def get_assets():
    """API endpoint to get supported assets"""
    return jsonify(engine.supported_assets)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend files"""
    if path == "" or not os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, 'index.html')
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
