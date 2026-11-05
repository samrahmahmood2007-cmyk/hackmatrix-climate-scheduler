import math
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def solve_lp(obs, est):
    t = obs["slot"]
    H = obs["horizon_slots"]
    cap = obs["capacity_units"]
    tariff = obs["tariff_gbp_per_kwh"]
    carbon_price = obs.get("carbon_price_gbp_per_kg", 1.0)

    active_jobs = [
        j for j in obs["jobs"]
        if j["remaining_units"] > 0 and j["deadline"] > t
    ]
    if not active_jobs:
        return {}

    variables = []
    costs = []

    for j_idx, job in enumerate(active_jobs):
        start_slot = max(job["release"], t)
        end_slot = min(job["deadline"], H)

        for s in range(start_slot, end_slot):
            var_idx = len(variables)
            cost = tariff[s] + carbon_price * (est[s] / 1000.0)
            variables.append((var_idx, j_idx, job["id"], s))
            costs.append(cost)

    num_vars = len(variables)
    if num_vars == 0:
        return None

    num_jobs = len(active_jobs)
    eq_rows = [j_idx for _, j_idx, _, _ in variables]
    eq_cols = [var_idx for var_idx, _, _, _ in variables]
    eq_data = np.ones(num_vars, dtype=np.float64)

    A_eq = coo_matrix((eq_data, (eq_rows, eq_cols)), shape=(num_jobs, num_vars))
    b_eq = np.array([j["remaining_units"] for j in active_jobs], dtype=np.float64)

    num_slots = H
    ub_rows = [s for _, _, _, s in variables]
    ub_cols = [var_idx for var_idx, _, _, _ in variables]
    ub_data = np.ones(num_vars, dtype=np.float64)

    A_ub = coo_matrix((ub_data, (ub_rows, ub_cols)), shape=(num_slots, num_vars))
    b_ub = np.full(num_slots, cap, dtype=np.float64)

    res = linprog(
        c=np.array(costs, dtype=np.float64),
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=(0, None),
        method="highs",
    )

    if not res.success:
        return None

    x_sol = res.x
    current_vars = [
        (var_idx, job_id, costs[var_idx])
        for var_idx, _, job_id, s in variables
        if s == t
    ]

    rem_lookup = {j["id"]: j["remaining_units"] for j in active_jobs}
    dispatch = {}

    for var_idx, job_id, _ in current_vars:
        val = int(math.floor(x_sol[var_idx] + 1e-6))
        val = min(val, rem_lookup[job_id])
        if val > 0:
            dispatch[job_id] = val

    total_dispatched = sum(dispatch.values())

    current_vars.sort(key=lambda item: item[2])
    while total_dispatched < cap:
        added_any = False
        for _, job_id, _ in current_vars:
            cur_val = dispatch.get(job_id, 0)
            if cur_val < rem_lookup[job_id]:
                dispatch[job_id] = cur_val + 1
                total_dispatched += 1
                added_any = True
                if total_dispatched >= cap:
                    break
        if not added_any:
            break

    return {str(k): int(v) for k, v in dispatch.items() if int(v) > 0}