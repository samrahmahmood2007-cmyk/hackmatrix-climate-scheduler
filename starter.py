"""Earliest-deadline starter. Replace decide with your causal scheduling policy."""
def decide(observation, state):
    capacity = observation['capacity_units']
    dispatch = {}
    for job in sorted(observation['jobs'], key=lambda j: (j['deadline'], j['id'])):
        amount = min(capacity, job['remaining_units'])
        if amount:
            dispatch[job['id']] = amount
            capacity -= amount
    return {'action': {'dispatch': dispatch}, 'state': state or {}}
