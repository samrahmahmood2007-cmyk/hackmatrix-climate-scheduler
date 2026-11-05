from safety import edf_dispatch

def decide(observation, state):
    if observation.get('done'):
        return {'action': {'dispatch': {}}, 'state': state or {}}
    result = edf_dispatch(observation)
    return {'action': {'dispatch': result}, 'state': state or {}}
