import time
import subprocess
import logging
import requests
import random
from pathlib import Path

# V3.3 Sovereign Bridge Automation Engine
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("auto_sync")

ROOT = Path(__file__).parent.parent
BASE_INTERVAL = 3 * 60 * 60  # 3 Hours
JITTER = 15 * 60             # 15 Minutes
POLL_INTERVAL = 60           # Check for remote trigger every 60s

# The bridge URL that the live dashboard writes to via sync.php
TRIGGER_URL = "https://www.bmwseals.com/sports/database/sync_trigger.txt"
LAST_TRIGGER_TS = 0

def run_sync(reason="Scheduled"):
    """
    Executes the full Intelligence Pipeline: Scrape -> Build -> Deploy
    """
    try:
        log.info(f"--- STARTING {reason.upper()} INTELLIGENCE SYNC ---")
        
        # 1. Scrape new RSS intel with stealth headers
        subprocess.run(["python", "engine/sports_scraper.py"], cwd=str(ROOT), check=True)
        
        # 2. Build production bundle (index.html + sports_news.js)
        subprocess.run(["python", "engine/build_dist.py"], cwd=str(ROOT), check=True)
        
        # 3. Deploy changed assets to bmwseals.com/sports
        subprocess.run(["python", "engine/remote_sync.py", "--dist"], cwd=str(ROOT), check=True)
        
        log.info(f"--- {reason.upper()} SYNC CYCLE COMPLETE ---")
        return True
    except Exception as e:
        log.error(f"INTELLIGENCE SYNC FAILED: {e}")
        return False

def check_remote_trigger():
    """
    Checks if a user on the live site clicked the 'SYNC' button
    """
    global LAST_TRIGGER_TS
    try:
        # Use a random query param to bypass any server-side or CDN caching
        resp = requests.get(f"{TRIGGER_URL}?v={time.time()}", timeout=5)
        if resp.status_code == 200:
            try:
                remote_ts = int(resp.text.strip())
                # Initial load: set the current remote TS as the baseline
                if LAST_TRIGGER_TS == 0:
                    log.info(f"Sync Bridge established. Current baseline TS: {remote_ts}")
                    LAST_TRIGGER_TS = remote_ts
                    return False
                
                # If the remote TS has increased, a user clicked SYNC
                if remote_ts > LAST_TRIGGER_TS:
                    log.info(f"Remote Sync Trigger Detected! (Remote: {remote_ts} > Local: {LAST_TRIGGER_TS})")
                    LAST_TRIGGER_TS = remote_ts
                    return True
            except ValueError:
                pass 
    except Exception:
        pass # Connectivity issues
    return False

if __name__ == "__main__":
    log.info("====================================================")
    log.info("Sovereign Stealth Bridge Engine V3.3 Initialized")
    log.info(f"Target: bmwseals.com/sports")
    log.info(f"Stealth Cycle: 3 hours (+/- 15m)")
    log.info(f"Bridge Polling: Every {POLL_INTERVAL} seconds")
    log.info("====================================================")
    
    # Run an initial sync on startup to ensure local data matches remote
    run_sync("Startup")
    
    last_scheduled_sync = time.time()
    next_scheduled_wait = BASE_INTERVAL + random.randint(-JITTER, JITTER)
    
    while True:
        current_time = time.time()
        
        # 1. Check for Manual Remote Trigger (Bridge)
        if check_remote_trigger():
            if run_sync("Remote Trigger"):
                # Reset the scheduled timer if we just did a manual sync
                last_scheduled_sync = current_time
                next_scheduled_wait = BASE_INTERVAL + random.randint(-JITTER, JITTER)
        
        # 2. Check for Scheduled Sync
        if (current_time - last_scheduled_sync) > next_scheduled_wait:
            if run_sync("Scheduled"):
                last_scheduled_sync = current_time
                next_scheduled_wait = BASE_INTERVAL + random.randint(-JITTER, JITTER)
        
        # Sleep for a minute before checking the bridge again
        time.sleep(POLL_INTERVAL)
