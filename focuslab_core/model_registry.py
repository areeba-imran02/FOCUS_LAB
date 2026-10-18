"""Conservative model discovery using the official Google GenAI SDK when available."""
from .config import DEFAULT_MODEL, FALLBACK_MODELS

def discover_models(client):
    """Return text-capable model IDs; discovery failure is intentionally non-fatal."""
    found=[]
    try:
        for model in client.models.list(config={"page_size":100}):
            name=getattr(model,"name","") or ""
            methods=getattr(model,"supported_actions",None) or getattr(model,"supported_generation_methods",None) or []
            if not name: continue
            mid=name.removeprefix("models/")
            low=mid.lower()
            if any(x in low for x in ("embedding", "aqa", "deprecated", "gemma")): continue
            if methods and not any("generatecontent" in str(x).lower() or "generate_content" in str(x).lower() for x in methods): continue
            found.append(mid)
    except Exception:
        return []
    return list(dict.fromkeys(found))

def candidates(client, preferred=None):
    discovered=discover_models(client)
    ordered=[]
    if preferred: ordered.append(preferred.strip())
    ordered.extend(discovered)
    ordered.extend(FALLBACK_MODELS)
    return list(dict.fromkeys(m for m in ordered if m and not any(x in m.lower() for x in ("embedding", "deprecated"))))[:8]
