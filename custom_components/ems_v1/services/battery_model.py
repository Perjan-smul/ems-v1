from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulationResult:
    capacity_kwh: int
    total_cost: float
    total_savings: float
    cycles: float


class BatteryModel:
    def __init__(self, efficiency: float = 0.92):
        self.efficiency = efficiency

    def simulate(self, capacity_kwh, pv, load, price):

        soc = 0.0
        max_soc = float(capacity_kwh)

        total_cost = 0.0
        total_savings = 0.0
        throughput = 0.0

        for i in range(24):

            surplus = pv[i] - load[i]

            if surplus > 0:
                charge = min(surplus, max_soc - soc)
                soc += charge * self.efficiency
                throughput += charge
            else:
                discharge = min(abs(surplus), soc)
                soc -= discharge
                supplied = discharge * self.efficiency
                throughput += discharge
                total_savings += supplied * price[i]

            grid_cost = max(load[i] - pv[i], 0)
            total_cost += grid_cost * price[i]

        cycles = throughput / (capacity_kwh + 1e-9)

        return SimulationResult(
            capacity_kwh=capacity_kwh,
            total_cost=total_cost,
            total_savings=total_savings,
            cycles=cycles,
        )
