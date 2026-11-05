"""Climate-tech scheduling challenge — final single-file submission.

Assembly rules:
  * Exactly ONE copy of each function. No duplicate definitions.
  * No imports between teammates' modules — everything lives here.
  * Function names and signatures are frozen by INTERFACES.md.
"""

import math

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


# === PASTE ZONE 1 — from carbon_cost.py (diya) ==============================
# Contract: def carbon_series(obs) -> numpy array
#   length obs['horizon_slots'], g/kWh, risk-buffered, ALL FINITE
def carbon_series(obs):
    return np.zeros(int(obs["horizon_slots"]), dtype=float)  # TEMP STUB
# === END PASTE ZONE 1 =======================================================


# === PASTE ZONE 2 — from lp_engine.py (samanth) =============================
# Contract: def solve_lp(obs, est) -> dict or None
#   {job_id: integer units} for slot obs['slot']; None if the solver fails
def solve_lp(obs, est):
    return None  # TEMP STUB -> forces the EDF fallback path
# === END PASTE ZONE 2 =======================================================


# === PASTE ZONE 3 — from safety.py (bhuvanesh) ==============================
# Contract: def edf_thumb_dispatch(obs) -> dict
def edf_dispatch(obs):
    return {}  # TEMP STUB
# === END PASTE ZONE 3 =======================================================


# === PASTE ZONE 4 — from safety.py (bhuvanesh) ==============================
# Contract: def clean_dispatch(dispatch, obs) -> dict
def clean_dispatch(dispatch, obs):
    return dispatch  # TEMP STUB
# === END PASTE ZONE 4 =======================================================


def decide(observation, state):
    """Called once per 30-minute slot. Must never raise."""
    obs = observation

    # Nothing left to schedule: hand back an empty, always-valid action.
    if obs.get("done"):
        return {"action": {"dispatch": {}}, "state": {}}

    try:
        est = carbon_series(obs)
        result = solve_lp(obs, est)
        # solve_lp returns None on solver failure -> fall back to EDF.
        if result is None:
            result = edf_dispatch(obs)
    except Exception:
        # Any raised exception -> fall back to EDF. A rejected action
        # wastes the whole slot, so we always return something valid.
        result = edf_dispatch(obs)

    result = clean_dispatch(result, obs)
    return {"action": {"dispatch": result}, "state": {}}
