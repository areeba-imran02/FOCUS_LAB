"""Deterministic trial generation. Timing in Streamlit is approximate, not lab-grade."""
import random
from dataclasses import dataclass, asdict
from typing import Optional

TARGET = "blue_circle"
NON_TARGETS = ("blue_square", "purple_circle", "purple_square")
CONDITIONS = ("quiet", "notifications")

@dataclass
class Trial:
    condition: str
    stimulus: str
    is_target: bool
    response: Optional[bool] = None
    reaction_ms: Optional[float] = None
    timed_out: bool = False

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

def make_trials(condition: str, seed=None):
    if condition not in CONDITIONS:
        raise ValueError("Unknown condition")
    rng = random.Random(seed)
    stimuli = [TARGET] * 12 + ["blue_square"] * 4 + ["purple_circle"] * 4 + ["purple_square"] * 4
    rng.shuffle(stimuli)
    return [Trial(condition, s, s == TARGET) for s in stimuli]

def make_session(seed=None):
    rng = random.Random(seed)
    order = list(CONDITIONS)
    rng.shuffle(order)
    return {"condition_order": order, "conditions": {c: [t.to_dict() for t in make_trials(c, rng.randrange(1_000_000_000))] for c in order}, "practice": 0, "active_condition": 0}

def practice_trial(seed=None):
    rng = random.Random(seed)
    return rng.choice([TARGET, *NON_TARGETS])
