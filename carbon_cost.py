import numpy as np
import math

# Risk sigma constant as specified by team requirements (can be tuned later: 0, 0.5, 1.0, 1.5)
RISK_SIGMA = 1.0

def carbon_series(obs):
    """
    Returns a numpy array of length obs['horizon_slots'], in g/kWh,
    with the risk buffer added.
    """
    horizon = obs.get('horizon_slots', 40)
    
    # 1. Create an empty numpy array filled with NaN for estimates, and zeros for uncertainty
    est = np.full(horizon, np.nan, dtype=float)
    unc = np.zeros(horizon, dtype=float)
    
    # 2. Fill from obs['forecast'] safely
    forecast = obs.get('forecast', [])
    for row in forecast:
        if not isinstance(row, dict):
            continue
        slot = row.get('slot')
        c_val = row.get('carbon_g_per_kwh')
        u_val = row.get('uncertainty_g_per_kwh', 0.0)
        
        try:
            s_int = int(slot)
            c_float = float(c_val)
            u_float = float(u_val)
            
            # Check validity and boundaries
            if 0 <= s_int < horizon and math.isfinite(c_float) and math.isfinite(u_float):
                est[s_int] = c_float
                unc[s_int] = max(0.0, u_float) # Uncertainty cannot be negative
        except (ValueError, TypeError):
            continue # Skip any bad or malformed rows cleanly
            
    # 3. Fallback for any slot still NaN using history or default 200.0
    history = obs.get('history', [])
    fallback_val = 200.0
    
    if history:
        # Get the last item in history
        last_item = history[-1]
        if isinstance(last_item, dict):
            try:
                hist_c = float(last_item.get('carbon_g_per_kwh', 200.0))
                if math.isfinite(hist_c):
                    fallback_val = hist_c
            except (ValueError, TypeError):
                pass
                
    # Fill remaining NaNs with the fallback value
    for i in range(horizon):
        if not math.isfinite(est[i]):
            est[i] = fallback_val
            
    # 4. Add the risk buffer: est = est + RISK_SIGMA * unc
    est = est + (RISK_SIGMA * unc)
    
    # 5. Ensure everything is finite and non-negative
    est = np.nan_to_num(est, nan=fallback_val, posinf=fallback_val, neginf=0.0)
    est = np.clip(est, 0.0, None)
    
    return est
