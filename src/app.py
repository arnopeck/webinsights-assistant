"""
WebInsights Assistant - App Module

This module provides the Flask application for the WebInsights Assistant system,
enabling web-based access to the analytics insights.
"""

import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

from src.webinsights_integration import WebInsightsAssistant

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WebInsightsApp")

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Create WebInsights Assistant
assistant = None

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze website data based on form input."""
    global assistant
    
    # Get form data
    property_id = request.form.get('property_id') or os.getenv('GA_PROPERTY_ID')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    credentials_path = request.form.get('credentials_path') or os.getenv('GA_CREDENTIALS_PATH')
    
    # Validate inputs
    if not property_id:
        return jsonify({"error": "No Google Analytics property ID provided"}), 400
    
    try:
        # Initialize assistant if not already done
        if assistant is None:
            assistant = WebInsightsAssistant(credentials_path)
            
            # Authenticate with Google Analytics
            if not assistant.authenticate_google_analytics():
                return jsonify({"error": "Failed to authenticate with Google Analytics"}), 401
        
        # Analyze website data
        results = assistant.analyze_website_data(property_id, start_date, end_date)
        
        # Generate report
        report_path = assistant.generate_collaborative_report(results, "html")
        
        # Return success response
        return jsonify({
            "success": True,
            "report_path": report_path,
            "message": "Analysis completed successfully"
        })
        
    except Exception as e:
        logger.error(f"Error analyzing website data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """API endpoint to get insights for a property."""
    global assistant
    
    # Get query parameters
    property_id = request.args.get('property_id') or os.getenv('GA_PROPERTY_ID')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    credentials_path = os.getenv('GA_CREDENTIALS_PATH')
    
    # Validate inputs
    if not property_id:
        return jsonify({"error": "No Google Analytics property ID provided"}), 400
    
    try:
        # Initialize assistant if not already done
        if assistant is None:
            assistant = WebInsightsAssistant(credentials_path)
            
            # Authenticate with Google Analytics
            if not assistant.authenticate_google_analytics():
                return jsonify({"error": "Failed to authenticate with Google Analytics"}), 401
        
        # Analyze website data
        results = assistant.analyze_website_data(property_id, start_date, end_date)
        
        # Return insights
        return jsonify({
            "insights": results.get("insights", {}),
            "recommendations": results.get("recommendations", {})
        })
        
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        return jsonify({"error": str(e)}), 500

def create_app(test_config=None):
    """Create and configure the Flask application."""
    if test_config:
        app.config.update(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
