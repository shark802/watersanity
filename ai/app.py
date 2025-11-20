"""
Alternative entry point for Heroku deployment
This file can be used if you want to deploy from the ai/ directory directly
"""
import sys
import os

# Add parent directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from ml_server import app

# This allows Heroku to use: web: gunicorn app:app
# Instead of: web: cd ai && gunicorn ml_server:app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

