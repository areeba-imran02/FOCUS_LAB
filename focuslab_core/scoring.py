"""Pure deterministic scoring for completed experiment trials."""
import statistics
from .experiment import Trial

def score_condition(trials):
    trials = [t if isinstance(t, Trial) else Trial.from_dict(t) for t in trials]
    targets = [t for t in trials if t.is_target]
    non_targets = [t for t in trials if not t.is_target]
    hits = sum(t.response is True for t in targets)
    misses = sum(t.response is False or t.timed_out or t.response is None for t in targets)
    false_alarms = sum(t.response is True for t in non_targets)
    correct_rejections = sum(t.response is False for t in non_targets)
    total = len(trials)
    correct = hits + correct_rejections
    rts = [float(t.reaction_ms) for t in targets if t.response is True and t.reaction_ms is not None and t.reaction_ms >= 0]
    return {"trials": total, "targets": len(targets), "non_targets": len(non_targets), "hits": hits, "misses": misses, "false_alarms": false_alarms, "correct_rejections": correct_rejections, "accuracy": correct / total if total else None, "median_rt_ms": statistics.median(rts) if rts else None, "completed": total > 0 and all(t.response is not None or t.timed_out for t in trials)}

def compare_conditions(quiet, notifications):
    q, n = score_condition(quiet), score_condition(notifications)
    return {"accuracy_difference": _diff(q["accuracy"], n["accuracy"]), "median_rt_difference_ms": _diff(q["median_rt_ms"], n["median_rt_ms"]), "miss_difference": n["misses"] - q["misses"], "false_alarm_difference": n["false_alarms"] - q["false_alarms"]}

def _diff(a, b):
    return None if a is None or b is None else b - a
