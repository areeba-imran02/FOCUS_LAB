from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
EVIDENCE_PATH = DATA_DIR / "evidence.json"
HISTORY_PATH = ROOT / ".focuslab_history.json"
MAX_INTAKE_CHARS = 2500
MAX_MODEL_ATTEMPTS = 3
DEFAULT_MODEL = "gemini-2.5-flash"
FALLBACK_MODELS = ("gemini-2.5-flash", "gemini-2.0-flash")

def load_evidence():
    with EVIDENCE_PATH.open(encoding="utf-8") as f:
        return json.load(f)
