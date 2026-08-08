"""
Entry point for the AI Career Connect application.
Run this file to start the Flask development server.
"""

import os
from app import create_app

# Default to 'development' for local runs. Set to 'production' on Render.
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    app.run(debug=(env == 'development'), port=5000)
