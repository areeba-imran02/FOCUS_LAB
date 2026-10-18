"""Optional local history helpers. Cloud filesystem persistence is not guaranteed."""
import json
from pathlib import Path
from datetime import datetime, timezone
from .config import HISTORY_PATH

def load_history(path=HISTORY_PATH):
    p=Path(path)
    if not p.exists(): return []
    try:
        data=json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data,list) else []
    except (OSError,json.JSONDecodeError): return []

def save_history(item,path=HISTORY_PATH):
    p=Path(path); rows=load_history(p); row=dict(item); row.setdefault("saved_at",datetime.now(timezone.utc).isoformat()); rows.append(row)
    p.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    return rows

def export_history(rows): return json.dumps(rows,ensure_ascii=False,indent=2).encode("utf-8")
def clear_history(path=HISTORY_PATH):
    p=Path(path)
    try: p.unlink()
    except FileNotFoundError: pass
