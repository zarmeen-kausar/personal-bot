import hashlib
import os
from pathlib import Path
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=True)

APP_USERNAME = os.getenv("APP_USERNAME", "demo")
APP_PASSWORD = os.getenv("APP_PASSWORD", "changeme")


def make_token(username: str, password: str) -> str:
    return hashlib.sha256(f"{username}:{password}:personal-bot".encode()).hexdigest()[:32]


VALID_TOKEN = make_token(APP_USERNAME, APP_PASSWORD)

app = FastAPI(title="Personal Bot Status")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str


@app.post("/api/login", response_model=LoginResponse)
def login(req: LoginRequest) -> LoginResponse:
    if req.username != APP_USERNAME or req.password != APP_PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    return LoginResponse(token=VALID_TOKEN)


def check_auth(authorization: Optional[str]) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token.")
    if authorization[len("Bearer "):] != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")


@app.get("/api/status")
def status(authorization: Optional[str] = Header(None)) -> dict:
    check_auth(authorization)

    log_dir = ROOT / "log"
    log_files = sorted(log_dir.glob("*.md"), reverse=True) if log_dir.exists() else []
    entries = []
    for f in log_files[:10]:
        entries.append({"date": f.stem, "content": f.read_text(encoding="utf-8")})

    return {
        "skill": {
            "name": "daily-wrapup",
            "trigger": "/daily-wrapup, or end-of-day phrases",
            "writes_to": "log/<YYYY-MM-DD>.md",
            "runs_found": len(log_files),
        },
        "loop": {
            "name": "daily-wrapup-6pm",
            "schedule": "Mon–Fri, 6 PM Asia/Karachi (cron 0 13 * * 1-5)",
            "routine_id": "trig_0173eVve9cZ2tfo6sPi4T7tk",
            "enabled": True,
            "last_fired_at": "2026-07-29T13:02:45Z",
            "next_run_at": "2026-07-30T13:01:43Z",
            "target_repo": "github.com/zarmeen-kausar/personal-bot",
            "snapshot_note": "Static snapshot verified via the routine API on 2026-07-30 — not live-polled by this page.",
        },
        "hook": {
            "matcher": "notes/",
            "event": "FileChanged",
            "action": "re-wakes Claude Code and runs /daily-wrapup",
        },
        "log_entries": entries,
    }


PUBLIC = ROOT / "public"
if PUBLIC.exists():
    app.mount("/public", StaticFiles(directory=str(PUBLIC)), name="public")

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(str(PUBLIC / "index.html"))


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8090"))
    uvicorn.run("server:app", host="0.0.0.0", port=port, log_level="info")
