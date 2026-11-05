import importlib.util, json
spec = importlib.util.spec_from_file_location("sol", "solution.py")
sol = importlib.util.module_from_spec(spec); spec.loader.exec_module(sol)

obs = {"slot": 0, "done": False, "horizon_slots": 40, "capacity": 4, "jobs": []}
out = sol.decide(obs, {})
print(out)

assert set(out.keys()) == {"action", "state"}
assert set(out["action"].keys()) == {"dispatch"}
assert isinstance(out["action"]["dispatch"], dict)
assert out == {"action": {"dispatch": {}}, "state": {}}
assert sol.decide({"done": True, "horizon_slots": 40}, {}) == {"action": {"dispatch": {}}, "state": {}}
assert len(sol.carbon_series(obs)) == 40
json.dumps(out)
print("WIRING OK")
