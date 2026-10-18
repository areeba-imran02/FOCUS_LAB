"""Bounded official Google GenAI integration. No credentials are stored here."""
import json, os, time
from .config import DEFAULT_MODEL, MAX_MODEL_ATTEMPTS
from .fallback import classify_error, local_fallback_plan
from .model_registry import candidates
from .models import FocusPlan

def get_api_key():
    try:
        import streamlit as st
        value=st.secrets.get("GEMINI_API_KEY", "")
        if value: return str(value).strip()
    except Exception: pass
    return os.environ.get("GEMINI_API_KEY", "").strip()

def _extract_json(text):
    text=text.strip()
    if text.startswith("```"):
        text=text.split("\n",1)[-1].rsplit("```",1)[0].strip()
    start=text.find("{"); end=text.rfind("}")
    if start < 0 or end < start: raise ValueError("No JSON object returned")
    return json.loads(text[start:end+1])

def generate_plan(intake, metrics=None, evidence=None, consent=False, timeout_seconds=18, max_attempts=MAX_MODEL_ATTEMPTS):
    evidence=evidence or []; metrics=metrics or {}
    if not consent:
        return FocusPlan.model_validate(local_fallback_plan(intake,metrics,evidence)), "Local fallback active — AI sharing was not approved.", []
    key=get_api_key()
    if not key:
        return FocusPlan.model_validate(local_fallback_plan(intake,metrics,evidence)), "API configuration required — local fallback active.", []
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return FocusPlan.model_validate(local_fallback_plan(intake,metrics,evidence)), "AI unavailable — google-genai is not installed in this environment.", []
    client=genai.Client(api_key=key, http_options=types.HttpOptions(timeout=int(timeout_seconds*1000)))
    preferred=""
    try:
        import streamlit as st
        preferred=str(st.secrets.get("GEMINI_MODEL", "")).strip()
    except Exception: pass
    if not preferred: preferred=os.environ.get("GEMINI_MODEL", "").strip()
    models=candidates(client,preferred)
    attempts=[]
    prompt={"task":"Create a practical focus plan using only supplied facts. Return JSON only matching FocusPlan fields: summary, steps[{title,minutes,rationale}], environment_changes, if_interrupted, evidence_ids, source. Do not invent experiment metrics or citations. Use only supplied evidence IDs. Keep steps within the user's available time. source must be gemini.","intake":intake,"experiment_metrics":metrics,"retrieved_evidence":evidence}
    for model in models[:max(1,min(int(max_attempts),4))]:
        try:
            response=client.models.generate_content(model=model, contents=json.dumps(prompt,ensure_ascii=False), config={"response_mime_type":"application/json","temperature":0.2,"max_output_tokens":1200})
            raw=_extract_json(response.text or "")
            raw["source"]="gemini"
            plan=FocusPlan.model_validate(raw)
            allowed={e["id"] for e in evidence}
            if any(i not in allowed for i in plan.evidence_ids): raise ValueError("Model returned an invalid evidence reference")
            total=sum(s.minutes for s in plan.steps)
            if total > int(intake.get("available_minutes",30)): raise ValueError("Plan exceeds available time")
            return plan, f"Gemini AI active — model: {model}.", attempts
        except Exception as exc:
            kind=classify_error(exc); attempts.append({"model":model,"category":kind})
            if kind in ("auth","quota","safety"): break
    plan=FocusPlan.model_validate(local_fallback_plan(intake,metrics,evidence))
    return plan, "Local fallback active — eligible Gemini attempts failed. Check configuration, quota, and model availability.", attempts
