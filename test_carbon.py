import json
import numpy as np
from carbon_cost import carbon_series

def test():
    # Load smoke.json from the same folder
    with open('smoke.json', 'r') as f:
        data = json.load(f)
        
    obs = data['examples'][0]['trace'][0]['observation']
    horizon = obs.get('horizon_slots', 40)
    
    result = carbon_series(obs)
    
    print("Result array:", result)
    assert len(result) == horizon, f"Length mismatch: {len(result)} vs {horizon}"
    assert np.all(np.isfinite(result)), "Result contains non-finite values!"
    assert np.all(result >= 0), "Result contains negative values!"
    
    mean_val = np.mean(result)
    print(f"Mean carbon value: {mean_val}")
    assert 50 <= mean_val <= 400, f"Mean value {mean_val} out of expected range [50, 400]"
    print("All carbon_cost tests PASSED successfully!")

if __name__ == '__main__':
    test()
