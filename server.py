import logging
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Setup
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("sports-news")

ROOT = Path(__file__).parent
app = FastAPI(title="Sovereign Sports Intelligence", version="1.0")

# Static File Serving
app.mount("/database", StaticFiles(directory=str(ROOT / "database")), name="database")

@app.get("/")
async def serve_dashboard():
    return FileResponse(str(ROOT / "web" / "index.html"))

@app.post("/api/sync")
async def sync_data():
    import subprocess
    log.info("Manual sync triggered...")
    subprocess.run(["python", "engine/sports_scraper.py"], cwd=str(ROOT))
    return {"status": "ok", "message": "Sports intelligence synchronized."}

if __name__ == "__main__":
    log.info("Sovereign Sports Intelligence starting...")
    log.info("Dashboard: http://localhost:5175")
    uvicorn.run(app, host="0.0.0.0", port=5175)
