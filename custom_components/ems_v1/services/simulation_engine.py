from __future__ import annotations

from typing import List
from .battery_model import BatteryModel


class SimulationEngine:
    def __init__(self):
        self.model = BatteryModel()

    def run_scenarios(self, capacities, pv, load, price):

        results = []

        for cap in capacities:
            r = self.model.simulate(cap, pv, load, price)
            results.append(r)

        results.sort(
            key=lambda r: r.total_savings - r.total_cost,
            reverse=True,
        )

        return results
