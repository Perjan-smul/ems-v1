from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class EMSCoordinator(DataUpdateCoordinator):
    """Central EMS coordinator (v1.2)."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry

        self._forecast_cache = None
        self._simulation_cache = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"ems_v1_2_{entry.entry_id}",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """
        Central update cycle:
        - fetch HA sensor data
        - run forecast engine
        - optionally run simulation
        - return aggregated state
        """

        pv_now = await self._get_pv_data()
        load_now = await self._get_load_data()
        price_now = await self._get_price_data()

        forecast = await self._build_forecast(pv_now, load_now, price_now)

        simulation = await self._run_simulation_if_enabled(forecast)

        return {
            "pv": pv_now,
            "load": load_now,
            "price": price_now,
            "forecast": forecast,
            "simulation": simulation,
        }

    # -----------------------------
    # Data acquisition layer
    # -----------------------------

    async def _get_pv_data(self):
        return {}

    async def _get_load_data(self):
        return {}

    async def _get_price_data(self):
        return {}

    # -----------------------------
    # v1.2 FORECAST HOOK
    # -----------------------------

    async def _build_forecast(self, pv, load, price):
        """
        Placeholder for v1.2 forecast engine hook.
        Later replaced by forecast_engine.py module.
        """

        return {
            "pv_forecast": pv,
            "load_forecast": load,
            "price_forecast": price,
        }

    # -----------------------------
    # v1.2 SIMULATION HOOK
    # -----------------------------

    async def _run_simulation_if_enabled(self, forecast):
        """
        Placeholder for simulation engine.
        Will be expanded in v1.2 module rollout.
        """

        if not self.entry.options.get("enable_simulation", True):
            return None

        return {
            "status": "stub",
            "scenarios": [5, 10, 15, 20],
        }

    # -----------------------------
    # optional cleanup
    # -----------------------------

    async def async_shutdown(self):
        """Safe shutdown hook for HA unload."""

        self._forecast_cache = None
        self._simulation_cache = None
