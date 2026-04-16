from __future__ import annotations

from typing import List

from .battery_model import BatteryModel, SimulationResult


class SimulationEngine:
    def __init__(self):
        self.model = BatteryModel()

    def run_scenarios(
        self,
        capacities: List[int],
        pv: List[float],
        load: List[float],
        price: List[float],
    ) -> List[SimulationResult]:

        results: List[SimulationResult] = []

        for cap in capacities:
            results.append(
                self.model.simulate(cap, pv, load, price)
            )

        results.sort(
            key=lambda r: r.total_savings - r.total_cost,
            reverse=True,
        )

        return results
