"""
app.py — Optional Challenge 2: Shareable Web Service
Expose the automation as a REST API using FastAPI.
"""

from fastapi import FastAPI
import subprocess

app = FastAPI(title="Automation API", description="Trigger Playwright automation via HTTP")

@app.get("/")
def root():
    return {"status": "ready", "message": "Send /run to start automation."}

@app.post("/run")
def run_task():
    try:
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        return {"success": True, "output": result.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}
