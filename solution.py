# solution.py - Assembled final pipeline for Hackmatrix 1.0 climate scheduler

from carbon_cost import carbon_series
from lp_engine import solve_lp
from safety import edf_dispatch, clean_dispatch

def decide(observation, state):
    """
    Main entry point for the platform.
    Uses rolling min-cost LP with risk buffer, falling back to EDF, 
    and passes through safety guardrails.
    """
    if observation.get('done'):
        return {'action': {'dispatch': {}}, 'state': state or {}}
        
    result = None
    try:
        est = carbon_series(observation)
        result = solve_lp(observation, est)
        if result is None:
            result = edf_dispatch(observation)
    except Exception:
        result = edf_dispatch(observation)
        
    result = clean_dispatch(result, observation)
    return {'action': {'dispatch': result}, 'state': state or {}}
