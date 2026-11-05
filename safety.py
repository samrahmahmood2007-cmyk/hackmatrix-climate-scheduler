def edf_dispatch(obs):
    """
    Earliest-Deadline-First fallback baseline.
    Sorts jobs by deadline, then by id, and allocates capacity greedily.
    """
    capacity_left = obs.get('capacity_units', 0)
    jobs = obs.get('jobs', [])
    
    # Sort jobs by (deadline, id)
    sorted_jobs = sorted(jobs, key=lambda j: (j.get('deadline', 0), j.get('id', '')))
    
    dispatch = {}
    for job in sorted_jobs:
        job_id = job.get('id')
        remaining = job.get('remaining_units', 0)
        
        if capacity_left <= 0:
            break
            
        amount = min(capacity_left, remaining)
        if amount > 0:
            dispatch[job_id] = int(amount)
            capacity_left -= amount
            
    return dispatch

def clean_dispatch(dispatch, obs):
    """
    Final guard pass to ensure the dispatch dict is completely valid and safe.
    Never raises an exception.
    """
    if not isinstance(dispatch, dict):
        dispatch = {}
        
    capacity_left = obs.get('capacity_units', 0)
    jobs = obs.get('jobs', [])
    
    # Create a lookup for remaining units and valid IDs
    valid_jobs = {}
    for job in jobs:
        j_id = job.get('id')
        rem = job.get('remaining_units', 0)
        if j_id is not None and rem > 0:
            valid_jobs[j_id] = rem
            
    cleaned = {}
    for job_id, val in dispatch.items():
        if job_id not in valid_jobs:
            continue
            
        try:
            val_int = int(val)
        except (ValueError, TypeError):
            continue
            
        if val_int <= 0:
            continue
            
        # Cap at job's remaining units
        max_allowed = valid_jobs[job_id]
        val_int = min(val_int, max_allowed)
        
        # Cap at remaining global capacity
        if capacity_left <= 0:
            break
        val_int = min(val_int, capacity_left)
        
        if val_int > 0:
            cleaned[job_id] = val_int
            capacity_left -= val_int
            
    return cleaned

def decide(observation, state):
    """
    The main glue function called by the team lead's solution.py.
    """
    if observation.get('done'):
        return {'action': {'dispatch': {}}, 'state': state or {}}
        
    result = None
    try:
        # Import teammate modules locally so missing files during early testing won't crash import
        from carbon_cost import carbon_series
        from lp_engine import solve_lp
        
        est = carbon_series(observation)
        result = solve_lp(observation, est)
        if result is None:
            result = edf_dispatch(observation)
    except Exception:
        result = edf_dispatch(observation)
        
    result = clean_dispatch(result, observation)
    return {'action': {'dispatch': result}, 'state': state or {}}
