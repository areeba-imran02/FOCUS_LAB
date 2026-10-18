"""Transparent descriptive analytics; no predictive model is trained."""
from .scoring import score_condition, compare_conditions
MIN_SESSIONS_FOR_EXPLORATORY_MODEL=20
def summarize_session(results):
    q=score_condition(results.get("quiet",[])); n=score_condition(results.get("notifications",[]))
    return {"quiet":q,"notifications":n,"comparison":compare_conditions(results.get("quiet",[]),results.get("notifications",[])),"complete":q["completed"] and n["completed"] and q["trials"]==24 and n["trials"]==24}
def exploratory_status(completed_sessions):
    if len(completed_sessions)<MIN_SESSIONS_FOR_EXPLORATORY_MODEL: return {"status":"Not enough data yet.","sessions":len(completed_sessions),"threshold":MIN_SESSIONS_FOR_EXPLORATORY_MODEL,"model_trained":False}
    return {"status":"Descriptive review only; no exploratory model is implemented.","sessions":len(completed_sessions),"threshold":MIN_SESSIONS_FOR_EXPLORATORY_MODEL,"model_trained":False}
