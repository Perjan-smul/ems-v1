from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class SimulationResult:
    capacity_kwh: int
    total_cost: float
    total_savings: float
    self_consumption: float
    cycles: float


class BatteryModel:
    def __init__(self, efficiency: float = 0.92):
        self.efficiency = efficiency

    def simulate(
        self,
        capacity_kwh: int,
        pv: List[float],
        load: List[float],
        price: List[float],
    ) -> SimulationResult:

        soc = 0.0
        max_soc = float(capacity_kwh)

        total_cost = 0.0
        total_savings = 0.0
        self_used = 0.0
        energy_throughput = 0.0

        for i in range(24):

            pv_i = pv[i]
            load_i = load[i]
            price_i = price[i]

            surplus = pv_i - load_i

            if surplus > 0:
                charge = min(surplus, max_soc - soc)
                soc += charge * self.efficiency
                energy_throughput += charge
                self_used += load_i

            else:
                deficit = abs(surplus)
                discharge = min(deficit, soc)
                soc -= discharge

                supplied = discharge * self.efficiency
                energy_throughput += discharge

                total_savings += supplied * price_i

            net_load = max(load_i - pv_i, 0)
            total_cost += net_load * price_i

        cycles = energy_throughput / (capacity_kwh + 1e-6)

        return SimulationResult(
            capacity_kwh=capacity_kwh,
            total_cost=total_cost,
            total_savings=total_savings,
            self_consumption=self_used,
            cycles=cycles,
        )
