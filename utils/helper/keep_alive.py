# =============================[ UPTIME ISSUE FIXED ]================================#
from os import environ
import logging
import requests
from flask import Flask
from threading import Thread
import pytz
import time
from apscheduler.schedulers.background import BackgroundScheduler
from utils.log import logger



RENDER_EXTERNAL_URL = environ.get("RENDER_EXTERNAL_URL", "http://localhost:5000")

def ping_self():
    url = f"{RENDER_EXTERNAL_URL}/alive"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Ping successful!")
        else:
            logger.error(f"Ping failed with status code {response.status_code}")
    except Exception as e:
        logger.error(f"Ping failed with exception: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.add_job(ping_self, 'interval', minutes=1)
    scheduler.start()

app = Flask(__name__)

@app.route('/alive')
def alive():
    return "I am alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run_flask).start()
