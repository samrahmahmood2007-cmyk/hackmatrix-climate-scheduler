"""Check a solution on archived public observations; not a counterfactual grader."""
import importlib.util
import copy
import math
import json
import sys
from pathlib import Path


def check_response(observation, response, known_jobs=None):
    """Check current work; replay also supplies completed jobs still in-window."""
    assert isinstance(response, dict) and set(response) == {'action', 'state'}
    action = response['action']
    assert isinstance(action, dict) and set(action) == {'dispatch'}
    dispatch = action['dispatch']
    assert isinstance(dispatch, dict)
    jobs = {j['id']: j for j in (observation['jobs'] if known_jobs is None else known_jobs)
            if j['release'] <= observation['slot'] < j['deadline']}
    assert all(k in jobs and type(v) is int and 0 <= v <= jobs[k]['remaining_units']
               for k, v in dispatch.items()), 'invalid job or work amount'
    assert sum(dispatch.values()) <= observation['capacity_units'], 'capacity exceeded'
    assert len(json.dumps(response).encode()) <= 1024 * 1024, 'response exceeds 1 MiB'


def climate_replay_observation(observation, previous, completed):
    from copy import deepcopy
    out = deepcopy(observation)
    out['previous_dispatch'] = ({k: deepcopy(previous[k]) for k in ('slot', 'dispatch', 'valid', 'units')}
                                if previous else None)
    out['completed_units'] = completed
    if 'evidence' in out:
        for key in ('jobs', 'previous_dispatch', 'completed_units'):
            out['evidence']['protected'][key] = deepcopy(out[key])
    return out


def replay(module, examples):
    """Replay public exogenous outcomes, reconstructing policy-dependent state.

    Only practice answers are read. Benchmarks never enter decide's observation.
    """
    results = []
    for example in examples:
        memory, previous = {}, None
        catalog = {}
        for frame in example['trace']:
            for j in frame['observation']['jobs']:
                catalog[j['id']] = {k: v for k, v in j.items() if k != 'remaining_units'}
        remaining = {k: j['units'] for k, j in catalog.items()}
        completed, joint, invalid, tariff_total, carbon_total = 0, 0, 0, 0, 0
        for frame in example['trace']:
            obs = copy.deepcopy(frame['observation'])
            t = obs['slot']
            obs['jobs'] = [{**j, 'remaining_units': remaining[jid]}
                           for jid, j in catalog.items()
                           if j['release'] <= t < j['deadline'] and remaining[jid] > 0]
            obs['jobs'].sort(key=lambda j: (j['release'], j['id']))
            obs['previous_dispatch'] = previous
            obs['completed_units'] = completed
            obs = climate_replay_observation(obs, previous, completed)
            response = module.decide(obs, memory)
            # Malformed response framing is a local failure; illegal world action
            # is rejected atomically just as it is by the trusted environment.
            assert isinstance(response, dict) and set(response) == {'action', 'state'}
            memory = response['state']
            try:
                check_response(obs, response, known_jobs=[
                    {**j, 'remaining_units': remaining[jid]} for jid, j in catalog.items()])
                dispatch, valid = response['action']['dispatch'], True
            except AssertionError:
                dispatch, valid = {}, False
                invalid += 1
            units = sum(dispatch.values())
            for jid, amount in dispatch.items():
                remaining[jid] -= amount
            actual = frame['outcome']['observed_carbon_g_per_kwh']
            tariff = units * obs['tariff_gbp_per_kwh'][t]
            carbon = units * actual / 1000
            completed += units
            tariff_total += tariff
            carbon_total += carbon
            joint += tariff + carbon
            previous = {'slot': t, 'dispatch': copy.deepcopy(dispatch), 'valid': valid,
                        'units': units, 'carbon_g': units * actual, 'tariff_gbp': tariff,
                        'observed_carbon_g_per_kwh': actual}
        total = sum(j['units'] for j in catalog.values())
        q = completed / total
        best = example['reference_full_service_joint_gbp']
        regret = max(0, joint - q * best) / best
        results.append({'score': 70 * q + 30 * q * math.exp(-regret / .20),
                        'completion_fraction': q, 'joint_cost_gbp': joint,
                        'tariff_gbp': tariff_total, 'carbon_kg': carbon_total,
                        'invalid_actions': invalid})
    return results


def main():
    source = Path(sys.argv[1] if len(sys.argv) > 1 else 'solution.py')
    examples_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / 'practice.json'
    spec = importlib.util.spec_from_file_location('student_solution', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    examples = json.loads(examples_path.read_text())
    results = replay(module, examples)
    summary = {key: sum(r[key] for r in results) / len(results) for key in results[0]}
    print(json.dumps({'public_cases': len(results), 'mean': summary}, indent=2))


if __name__ == '__main__':
    main()
