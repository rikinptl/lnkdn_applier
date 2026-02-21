"""
Web app for LinkedIn Auto Job Applier: form-based config and pipeline start/stop.
Supports Google sign-in via Supabase; config and applied jobs stored per user.
"""
import os
import json
import csv
import subprocess
import sys
import signal

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from config_io import (
    read_config_from_reference,
    write_all_config,
    get_default_config,
    REFERENCE_DIR,
)
from auth_supabase import get_user_id_from_request, require_auth
from supabase_client import get_supabase

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

# On Vercel, filesystem is read-only except /tmp; pipeline (subprocess) is not available
IS_VERCEL = os.environ.get("VERCEL") == "1"
CONFIG_JSON = os.path.join("/tmp" if IS_VERCEL else os.path.dirname(os.path.abspath(__file__)), "config.json")
APPLIED_CSV = os.path.join(REFERENCE_DIR, "all excels", "all_applied_applications_history.csv")

# Global subprocess handle for the bot (one at a time; not used on Vercel)
_bot_process = None


def _load_config() -> dict:
    if os.path.exists(CONFIG_JSON):
        try:
            with open(CONFIG_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    if IS_VERCEL or not os.path.isdir(REFERENCE_DIR):
        return get_default_config()
    return read_config_from_reference()


def _save_config(data: dict) -> None:
    with open(CONFIG_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


def _get_config_for_user(user_id: str) -> dict:
    """Load config from Supabase for user_id."""
    sb = get_supabase()
    if not sb:
        return get_default_config()
    try:
        r = sb.table("user_config").select("config").eq("user_id", user_id).execute()
        if r.data and len(r.data) > 0 and r.data[0].get("config"):
            return r.data[0]["config"]
    except Exception:
        pass
    return get_default_config()


def _upsert_config_for_user(user_id: str, config: dict) -> None:
    """Save config to Supabase for user_id."""
    from datetime import datetime, timezone
    sb = get_supabase()
    if not sb:
        return
    try:
        sb.table("user_config").upsert(
            {"user_id": user_id, "config": config, "updated_at": datetime.now(timezone.utc).isoformat()},
            on_conflict="user_id",
        ).execute()
    except Exception:
        pass


@app.route("/api/auth/env", methods=["GET"])
def auth_env():
    """Return public Supabase URL and anon key for frontend client (safe to expose)."""
    url = os.environ.get("SUPABASE_URL", "")
    anon = os.environ.get("SUPABASE_ANON_KEY", "")
    return jsonify({"SUPABASE_URL": url, "SUPABASE_ANON_KEY": anon})


@app.route("/api/config", methods=["GET"])
def get_config():
    """Return config: from Supabase if signed in, else from file/reference."""
    try:
        user_id = get_user_id_from_request()
        if user_id:
            config = _get_config_for_user(user_id)
            return jsonify(config)
        config = _load_config()
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/config", methods=["PUT", "POST"])
def save_config():
    """Save config: to Supabase if signed in, else to file (merge with existing)."""
    try:
        user_id = get_user_id_from_request()
        incoming = request.get_json() or {}
        if user_id:
            current = _get_config_for_user(user_id)
            for section in ("personals", "questions", "search", "secrets", "settings"):
                if section in incoming and isinstance(incoming[section], dict):
                    current.setdefault(section, {}).update(incoming[section])
            _upsert_config_for_user(user_id, current)
            return jsonify(current)
        current = _load_config()
        for section in ("personals", "questions", "search", "secrets", "settings"):
            if section in incoming and isinstance(incoming[section], dict):
                current.setdefault(section, {}).update(incoming[section])
        _save_config(current)
        return jsonify(current)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/config/load-from-reference", methods=["POST"])
def load_from_reference():
    """Reload config from reference repo. Saves to Supabase if signed in, else to file. On Vercel returns defaults."""
    try:
        if IS_VERCEL or not os.path.isdir(REFERENCE_DIR):
            config = get_default_config()
        else:
            config = read_config_from_reference()
        user_id = get_user_id_from_request()
        if user_id:
            _upsert_config_for_user(user_id, config)
        else:
            _save_config(config)
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/applied-jobs", methods=["GET"])
def get_applied_jobs():
    """Return applied jobs: from Supabase if signed in, else from reference CSV if present."""
    try:
        user_id = get_user_id_from_request()
        if user_id:
            sb = get_supabase()
            if sb:
                r = sb.table("applied_jobs").select(
                    "job_id, title, company, hr_name, hr_link, job_link, external_job_link, date_applied"
                ).eq("user_id", user_id).order("created_at", desc=True).execute()
                jobs = [
                    {
                        "Job_ID": row.get("job_id"),
                        "Title": row.get("title"),
                        "Company": row.get("company"),
                        "HR_Name": row.get("hr_name"),
                        "HR_Link": row.get("hr_link"),
                        "Job_Link": row.get("job_link"),
                        "External_Job_link": row.get("external_job_link"),
                        "Date_Applied": row.get("date_applied"),
                    }
                    for row in (r.data or [])
                ]
                return jsonify(jobs)
            return jsonify([])
        if os.path.exists(APPLIED_CSV):
            jobs = []
            with open(APPLIED_CSV, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    jobs.append({
                        "Job_ID": row.get("Job ID"),
                        "Title": row.get("Title"),
                        "Company": row.get("Company"),
                        "HR_Name": row.get("HR Name"),
                        "HR_Link": row.get("HR Link"),
                        "Job_Link": row.get("Job Link"),
                        "External_Job_link": row.get("External Job link"),
                        "Date_Applied": row.get("Date Applied"),
                    })
            return jsonify(jobs)
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/applied-jobs/sync", methods=["POST"])
@require_auth
def sync_applied_jobs(user_id):
    """Read reference CSV and upsert rows into Supabase applied_jobs for this user."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 503
    if not os.path.exists(APPLIED_CSV):
        return jsonify({"error": "No applied jobs file found", "synced": 0}), 404
    try:
        rows = []
        with open(APPLIED_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({
                    "user_id": user_id,
                    "job_id": (row.get("Job ID") or "").strip(),
                    "title": (row.get("Title") or "").strip(),
                    "company": (row.get("Company") or "").strip(),
                    "hr_name": (row.get("HR Name") or "").strip(),
                    "hr_link": (row.get("HR Link") or "").strip(),
                    "job_link": (row.get("Job Link") or "").strip(),
                    "external_job_link": (row.get("External Job link") or "").strip(),
                    "date_applied": (row.get("Date Applied") or "").strip(),
                })
        if not rows:
            return jsonify({"synced": 0, "message": "CSV empty"})
        sb.table("applied_jobs").upsert(rows, on_conflict="user_id,job_id").execute()
        return jsonify({"synced": len(rows)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pipeline/status", methods=["GET"])
def pipeline_status():
    """Return whether the bot is running and optional PID. On Vercel pipeline is never running."""
    if IS_VERCEL:
        return jsonify({"running": False, "vercel": True})
    global _bot_process
    if _bot_process is None:
        return jsonify({"running": False})
    if _bot_process.poll() is not None:
        _bot_process = None
        return jsonify({"running": False})
    return jsonify({"running": True, "pid": _bot_process.pid})


@app.route("/api/pipeline/start", methods=["POST"])
def pipeline_start():
    """Write config to reference, then start runAiBot.py. On Vercel returns 503 (run locally)."""
    if IS_VERCEL:
        return jsonify({
            "error": "Pipeline cannot run on Vercel. Run the app locally to start/stop the bot.",
            "vercel": True,
        }), 503
    global _bot_process
    if _bot_process is not None and _bot_process.poll() is None:
        return jsonify({"error": "Pipeline already running", "running": True}), 409
    body = request.get_json() or {}
    config = body.get("config") if isinstance(body.get("config"), dict) else None
    if not config:
        config = _load_config()
    try:
        write_all_config(config)
    except Exception as e:
        return jsonify({"error": f"Failed to write config: {e}"}), 500

    python = sys.executable
    run_script = os.path.join(REFERENCE_DIR, "runAiBot.py")
    if not os.path.exists(run_script):
        return jsonify({"error": "reference/runAiBot.py not found"}), 500

    try:
        _bot_process = subprocess.Popen(
            [python, run_script],
            cwd=REFERENCE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        )
        return jsonify({"running": True, "pid": _bot_process.pid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/pipeline/stop", methods=["POST"])
def pipeline_stop():
    """Stop the running bot process."""
    global _bot_process
    if _bot_process is None:
        return jsonify({"running": False, "message": "No pipeline was running"})
    try:
        if os.name == "nt":
            _bot_process.terminate()
        else:
            os.kill(_bot_process.pid, signal.SIGTERM)
        _bot_process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        _bot_process.kill()
    except Exception:
        try:
            _bot_process.kill()
        except Exception:
            pass
    _bot_process = None
    return jsonify({"running": False, "message": "Pipeline stopped"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
