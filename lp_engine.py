import numpy as np
import scipy.optimize as opt
import math

def solve_lp(obs, est):
    capacity = obs.get('capacity_units', 4)
    jobs = obs.get('jobs', [])
    if not jobs:
        return {}
    n_jobs = len(jobs)
    c = est[:n_jobs] if n_jobs <= len(est) else np.pad(est, (0, n_jobs - len(est)), 'edge')
    
    A_ub = np.ones((1, n_jobs))
    b_ub = np.array([capacity])
    bounds = [(0, job.get('remaining_units', 0)) for job in jobs]
    res = opt.linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    dispatch = {}
    if res.success and res.x is not None:
        for i, job in enumerate(jobs):
            j_id = job.get('id')
            val = int(round(res.x[i]))
            if val > 0:
                dispatch[j_id] = val
                
    # Fallback to EDF fill if LP dispatches 0 while capacity and jobs remain
    if sum(dispatch.values()) == 0 and capacity > 0:
        sorted_jobs = sorted(jobs, key=lambda j: (j.get('deadline', 0), j.get('id', '')))
        cap_left = capacity
        for job in sorted_jobs:
            if cap_left <= 0:
                break
            j_id = job.get('id')
            rem = job.get('remaining_units', 0)
            amount = min(cap_left, rem)
            if amount > 0:
                dispatch[j_id] = int(amount)
                cap_left -= amount
                
    return dispatch
