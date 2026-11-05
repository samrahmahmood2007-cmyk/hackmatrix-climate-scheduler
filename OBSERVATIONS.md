# Observation guide — frozen v6 rehearsal

Submit solution.py with decide(observation, state), returning action and state.
Preparation, feature engineering and decisions belong in that runnable pipeline.
You may compare algorithms and use any causal strategy consistent with the action
schema. Source examples and local checks are development aids;
only portal submissions reveal validation performance. Final results stay private
to organizers. See EVENT_RULES.md for limits, schedule and 20/30/50 phase weights.

Schedule flexible jobs within their release, deadline and capacity constraints.
Top-level operational fields, history and forecast remain available. evidence contains protected,
measurement_records, forecast_records and target_slots. Normalize kgCO2/kWh to gCO2/kWh by
multiplying by 1000; reject nonfinite values. Use record identity and source/issue metadata when
handling deliveries. Measurements must have slot earlier than the decision and available_slot
no later than it. Forecasts were produced only from evidence available at issued_slot; newer
does not guarantee greater accuracy. The supplied forecast uses the latest available vintage.
You may estimate another causal forecast and use any feasible dispatch policy. The public replay
checker reconstructs your policy's work state using published practice outcomes. Use portal
practice runs to check the complete submission protocol. Historical carbon values are estimates; jobs, tariffs, capacity, forecasts and operational timing are scenario assumptions.
