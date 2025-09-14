from flask import Flask, render_template, url_for, redirect, abort
import json
from pathlib import Path

app = Flask(__name__)

# --- Chris JSON setup (safer path + trim IDs) ---
BASE_DIR = Path(__file__).parent.resolve()
SCENES_FILE = BASE_DIR / "static" / "data" / "scenes_chris.json"

def _load_chris():
    with SCENES_FILE.open(encoding="utf-8") as f:
        raw = json.load(f)
    # make sure IDs don’t have stray spaces
    return {str(s["scene_id"]).strip(): s for s in raw}

try:
    CHRIS = _load_chris()
except FileNotFoundError:
    CHRIS = {}

def get_chris(scene_id: str) -> dict:
    key = str(scene_id).strip()
    try:
        return CHRIS[key]
    except KeyError:
        abort(404, f"Scene {key} not found")

# --- Crossroads & fixed paths ---
@app.get("/")
def home():
    return render_template("home.html", title="The Crossroads", theme="crossroads")

@app.get("/north")
def north_path():
    return redirect(url_for("chris_start"))

@app.get("/east")
def east_path():
    return render_template("east.html", theme="travis", title="East Path (Travis)")

@app.get("/south")
def south_path():
    return render_template("south.html", theme="charlie", title="South Path (Charlie)")

@app.get("/west")
def west_path():
    return render_template("west.html", theme="trey", title="West Path (Trey)")

# --- Chris dynamic routes ---
@app.get("/chris")
def chris_start():
    # Shortcut: always start at N-001
    return redirect(url_for("scene_chris", scene_id="N-001"))

@app.get("/chris/<scene_id>")
def scene_chris(scene_id):
    scene = get_chris(scene_id)
    return render_template("scene.html", scene=scene, title=scene.get("title"), theme="chris")

from flask import request

@app.get("/death")
def death():
    msg = request.args.get("msg") or "You slip at the last moment and fall to your death. That is the end of your story."
    return render_template("death.html", title="You Died", msg=msg, theme="chris")


# --- Main entry ---
if __name__ == "__main__":
    app.run(debug=True)
