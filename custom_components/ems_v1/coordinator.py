from __future__ import annotations

from typing import Dict, Any

from ..services.forecast_engine import ForecastEngine
from ..services.simulation_engine import SimulationEngine
from ..services.decision_engine import DecisionEngine

from ..learning.pv_learning import PVLearning
from ..learning.load_learning import LoadLearning
from ..storage.memory import EMSMemory
from .state import EMSState


class EMSPipeline:
    """EMS v2 pipeline with learning."""

    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

        self.forecast_engine = ForecastEngine(hass, entry)
        self.simulation_engine = SimulationEngine()
        self.decision_engine = DecisionEngine()

        # learning
        self.memory = EMSMemory()
        self.pv_learning = PVLearning(self.memory)
        self.load_learning = LoadLearning(self.memory)

        self.state = EMSState()

    async def run(self, inputs: Dict[str, Any]):

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
        # 2. LEARNING UPDATE (current hour)
        # -------------------------
        actual_pv = inputs.get("pv_now", 0.0)
        actual_load = inputs.get("load_now", 0.0)

        if forecast["pv_kw"]:
            self.pv_learning.update(actual_pv, forecast["pv_kw"][0])

        if forecast["load_kw"]:
            self.load_learning.update(actual_load, forecast["load_kw"][0])

        # -------------------------
        # 3. APPLY CORRECTION
        # -------------------------
        forecast["pv_kw"] = self.pv_learning.correct(forecast["pv_kw"])
        forecast["load_kw"] = self.load_learning.correct(forecast["load_kw"])

        # -------------------------
        # 4. SIMULATION
        # -------------------------
        sim_raw = self.simulation_engine.run_scenarios(
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
            for r in sim_raw
        ]

        # -------------------------
        # 5. DECISION
        # -------------------------
        decision = self.decision_engine.decide(
            forecast=forecast,
            simulation=simulation,
        )

        # -------------------------
        # 6. STATE UPDATE
        # -------------------------
        self.state.update(decision, forecast)

        return {
            "forecast": forecast,
            "simulation": simulation,
            "action": decision,
            "learning": {
                "pv_bias": self.memory.pv_bias(),
                "load_bias": self.memory.load_bias(),
            },
        }
