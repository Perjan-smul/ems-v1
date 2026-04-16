from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .services.forecast_engine import ForecastEngine

_LOGGER = logging.getLogger(__name__)


class EMSCoordinator(DataUpdateCoordinator):
    """EMS V1.2 central coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):

        self.hass = hass
        self.entry = entry

        self.forecast_engine = ForecastEngine(hass, entry)

        self._forecast_cache = None
        self._simulation_cache = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"ems_v1_2_{entry.entry_id}",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):

        pv = await self._get_pv_data()
        load = await self._get_load_data()
        price = await self._get_price_data()

        forecast = await self.forecast_engine.build(
            pv, load, price
        )

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
    # CLEAN SHUTDOWN
    # -------------------------

    async def async_shutdown(self):
        self._forecast_cache = None
        self._simulation_cache = None
