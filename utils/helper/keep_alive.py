import logging
import requests
from flask import Flask
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from os import environ
import pytz

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO)

# Get port from environment variable (for Render) or default to 10000
port = int(environ.get("PORT", 10000))

# Set the URL to ping, using the Render external URL or default to localhost
RENDER_EXTERNAL_URL = environ.get("RENDER_EXTERNAL_URL", f"http://localhost:{port}")

def ping_self():
    """Ping the /alive endpoint to keep the instance active."""
    url = f"{RENDER_EXTERNAL_URL}/alive"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("Pinging myself - Ping successful!")
        else:
            logging.error(f"Ping failed with status code {response.status_code}")
    except Exception as e:
        logging.error(f"Ping failed with exception: {e}")

def start_scheduler():
    """Start a background scheduler to ping every 50 seconds."""
    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.add_job(ping_self, 'interval', seconds=50)
    scheduler.start()

# Initialize Flask app
app = Flask(__name__)

@app.route('/alive')
def alive():
    """Endpoint to respond to ping requests."""
    return "I am alive!"

def run_flask():
    """Run the Flask app on the specified port."""
    app.run(host='0.0.0.0', port=port)

# Start Flask in a background thread
Thread(target=run_flask).start()

