from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .services.forecast_engine import ForecastEngine
from .services.simulation_engine import SimulationEngine

_LOGGER = logging.getLogger(__name__)


class EMSCoordinator(DataUpdateCoordinator):
    """EMS V1.2 central coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):

        self.hass = hass
        self.entry = entry

        # Engines
        self.forecast_engine = ForecastEngine(hass, entry)
        self.simulation_engine = SimulationEngine()

        # caches (future use)
        self._forecast_cache = None
        self._simulation_cache = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"ems_v1_2_{entry.entry_id}",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):

        # -------------------------
        # 1. DATA ACQUISITION
        # -------------------------
        pv = await self._get_pv_data()
        load = await self._get_load_data()
        price = await self._get_price_data()

        # -------------------------
        # 2. FORECAST LAYER
        # -------------------------
        forecast = await self.forecast_engine.build(
            pv, load, price
        )

        # -------------------------
        # 3. SIMULATION LAYER
        # -------------------------
        simulation = None

        if self.entry.options.get("enable_simulation", True):

            results = self.simulation_engine.run_scenarios(
                capacities=[5, 10, 15, 20],
                pv=forecast.pv_kw,
                load=forecast.load_kw,
                price=forecast.price_eur,
            )

            simulation = [
                {
                    "capacity_kwh": r.capacity_kwh,
                    "total_savings": round(r.total_savings, 3),
                    "total_cost": round(r.total_cost, 3),
                    "cycles": round(r.cycles, 3),
                    "roi": round(r.total_savings - r.total_cost, 3),
                }
                for r in results
            ]

        # -------------------------
        # 4. RETURN STATE
        # -------------------------
        return {
            "pv": pv,
            "load": load,
            "price": price,
            "forecast": {
                "pv_kw": forecast.pv_kw,
                "load_kw": forecast.load_kw,
                "price_eur": forecast.price_eur,
                "hours": forecast.hours,
            },
            "simulation": simulation,
        }

    # -------------------------
    # DATA SOURCES (stubs)
    # -------------------------

    async def _get_pv_data(self):
        return self.hass.data.get("ems_pv", {})

    async def _get_load_data(self):
        return self.hass.data.get("ems_load", {"avg": 0.5})

    async def _get_price_data(self):
        return self.hass.data.get("ems_price", {"avg": 0.25})

    # -------------------------
    # CLEANUP
    # -------------------------

    async def async_shutdown(self):
        self._forecast_cache = None
        self._simulation_cache = None
