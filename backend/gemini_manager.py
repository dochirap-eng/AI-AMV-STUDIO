import os, json, time, random, requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORAGE = ROOT / "storage"
TEMP_DIR = STORAGE / "temp"
LOGS_DIR = STORAGE / "logs"
MODEL_POOL_PATH = Path(__file__).resolve().parent / "model_pool.json"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / "gemini_manager.log"

def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line)
    with open(log_file, "a") as f:
        f.write(line + "\n")

def check_site(url):
    """Check if a free AI model site is reachable"""
    try:
        r = requests.head(url, timeout=5)
        return r.status_code < 400
    except:
        return False

def load_models():
    if MODEL_POOL_PATH.exists():
        return json.load(open(MODEL_POOL_PATH))
    return []

def save_models(models):
    with open(MODEL_POOL_PATH, "w") as f:
        json.dump(models, f, indent=2)

def update_model_pool():
    models = load_models()
    log("🔍 Gemini: Checking model pool updates...")

    for model in models:
        url = model.get("link")
        if not url:
            continue
        live = check_site(url)
        status = "✅ OK" if live else "❌ DOWN"
        log(f"🧠 Checked: {model['name']} → {status}")
        model["active"] = live

    # auto add dummy new model (simulate research)
    new_model = {
        "name": f"AutoFound AI {int(time.time())}",
        "link": "https://example-ai-lab.net/",
        "type": random.choice(["🎵 Audio", "🎥 Video", "💬 Text"]),
        "description": "Auto-discovered backup model.",
        "active": True
    }
    models.append(new_model)
    save_models(models)
    log(f"🆕 Added new model: {new_model['name']}")
    log("✅ Model pool updated successfully.")

def deep_sync_edit_plans():
    """Reads all edit_plan.json and enriches them with timing info"""
    plans = list(TEMP_DIR.glob("*_edit_plan.json"))
    if not plans:
        return
    for p in plans:
        try:
            data = json.load(open(p))
            data["synced"] = time.time()
            data["effects"].append({
                "type": "glow",
                "intensity": random.randint(1, 5)
            })
            json.dump(data, open(p, "w"), indent=2)
            log(f"✨ Synced plan: {p.name}")
        except Exception as e:
            log(f"⚠️ Error syncing {p.name}: {e}")

def run_research_loop():
    log("♻️ Gemini Deep Sync Active — AI Research + Edit Plan Enrichment")
    while True:
        update_model_pool()
        deep_sync_edit_plans()
        time.sleep(60)  # run every 1 min

if __name__ == "__main__":
    run_research_loop()
