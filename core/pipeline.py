from __future__ import annotations

from typing import Dict, Any

from ..services.forecast_engine import ForecastEngine
from ..services.simulation_engine import SimulationEngine
from ..services.decision_engine import DecisionEngine
from .state import EMSState


class EMSPipeline:
    """EMS v2 pipeline orchestrator."""

    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

        self.forecast_engine = ForecastEngine(hass, entry)
        self.simulation_engine = SimulationEngine()
        self.decision_engine = DecisionEngine()

        self.state = EMSState()

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:

        # -------------------------
        # 1. FORECAST
        # -------------------------
        forecast_obj = await self.forecast_engine.build(
            inputs["pv"],
            inputs["load"],
            inputs["price"],
        )

        forecast = {
            "pv_kw": forecast_obj.pv_kw,
            "load_kw": forecast_obj.load_kw,
            "price_eur": forecast_obj.price_eur,
            "hours": forecast_obj.hours,
        }

        # -------------------------
        # 2. SIMULATION
        # -------------------------
        simulation_raw = self.simulation_engine.run_scenarios(
            capacities=[5, 10, 15, 20],
            pv=forecast["pv_kw"],
            load=forecast["load_kw"],
            price=forecast["price_eur"],
        )

        simulation = [
            {
                "capacity_kwh": r.capacity_kwh,
                "savings": r.total_savings,
                "cost": r.total_cost,
                "cycles": r.cycles,
                "roi": r.total_savings - r.total_cost,
            }
            for r in simulation_raw
        ]

        # -------------------------
        # 3. DECISION
        # -------------------------
        decision = self.decision_engine.decide(
            forecast=forecast,
            simulation=simulation,
        )

        # -------------------------
        # 4. STATE UPDATE
        # -------------------------
        self.state.update(decision, forecast)

        return {
            "forecast": forecast,
            "simulation": simulation,
            "action": decision,
        }
