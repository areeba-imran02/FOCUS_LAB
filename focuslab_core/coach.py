"""Bounded Focus Coach Agent: validated tools + retrieval + structured plan."""
from .evidence import retrieve_evidence, validate_evidence_ids
from .fallback import local_fallback_plan
from .gemini_client import generate_plan
from .models import Intake, FocusPlan

def get_user_context(intake): return Intake.model_validate(intake).model_dump()
def get_experiment_metrics(results):
    if not isinstance(results, dict): return {}
    return {k:v for k,v in results.items() if k in ("quiet","notifications","comparison")}
def retrieve_tool(query): return retrieve_evidence(query,k=3)
def calculate_time_budget(minutes):
    minutes=int(minutes)
    if not 5 <= minutes <= 240: raise ValueError("Minutes must be between 5 and 240")
    return {"available_minutes":minutes,"work_block_minutes":max(3,round(minutes*.65)),"review_minutes":max(2,minutes-max(3,round(minutes*.65)))}
def validate_focus_plan(plan, intake, evidence):
    result=FocusPlan.model_validate(plan)
    validate_evidence_ids(result.evidence_ids, evidence)
    if sum(s.minutes for s in result.steps) > int(intake["available_minutes"]): raise ValueError("Plan exceeds available time")
    return result
def run_focus_coach(intake, metrics=None, consent=False):
    context=get_user_context(intake); query=" ".join([context.get("problem", ""),context.get("task", "")," ".join(context.get("distractions", []))])
    evidence=retrieve_tool(query)
    plan,status,attempts=generate_plan(context,get_experiment_metrics(metrics),evidence,consent=consent)
    return {"plan":plan,"status":status,"attempts":attempts,"evidence":evidence,"tools_used":["get_user_context","get_experiment_metrics","retrieve_evidence","calculate_time_budget","validate_focus_plan"]}
