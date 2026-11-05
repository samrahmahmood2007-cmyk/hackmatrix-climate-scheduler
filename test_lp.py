import json
import time
import numpy as np
from lp_engine import solve_lp

with open("smoke.json", "r") as f:
    smoke = json.load(f)

examples = smoke["examples"] if isinstance(smoke, dict) and "examples" in smoke else smoke
obs = examples[0]["trace"][0]["observation"]
est = np.zeros(40)

t0 = time.perf_counter()
res = solve_lp(obs, est)
dt = time.perf_counter() - t0

assert isinstance(res, dict), f"Expected dict, got {type(res)}"
assert all(type(v) is int for v in res.values()), "All values must be exact Python ints"
assert sum(res.values()) <= obs["capacity_units"], "Exceeded slot capacity"

jobs_by_id = {j["id"]: j["remaining_units"] for j in obs["jobs"]}
for job_id, v in res.items():
    assert job_id in jobs_by_id, f"Unknown job_id {job_id}"
    assert 0 <= v <= jobs_by_id[job_id], f"Invalid units {v} for job {job_id}"

print(f"Dispatched: {res} (Total: {sum(res.values())} units)")
print(f"Runtime: {dt:.4f}s — ALL TESTS PASSED!")