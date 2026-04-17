from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .core.pipeline import EMSPipeline
from .services.forecast_engine import ForecastEngine

_LOGGER = logging.getLogger(__name__)


class EMSCoordinator(DataUpdateCoordinator):
    """EMS V2 coordinator with fallback."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):

        self.hass = hass
        self.entry = entry

        self.pipeline = EMSPipeline(hass, entry)

        # fallback (v1)
        self.forecast_engine = ForecastEngine(hass, entry)

        super().__init__(
            hass,
            _LOGGER,
            name=f"ems_v2_{entry.entry_id}",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):

        pv = await self._get_pv_data()
        load = await self._get_load_data()
        price = await self._get_price_data()

        use_v2 = self.entry.options.get("use_v2_pipeline", True)

        # -------------------------
        # V2 PIPELINE
        # -------------------------
        if use_v2:

            result = await self.pipeline.run(
                {
                    "pv": pv,
                    "load": load,
                    "price": price,
                }
            )

            return {
                "pv": pv,
                "load": load,
                "price": price,
                "forecast": result["forecast"],
                "simulation": result["simulation"],
                "action": result["action"],
            }

        # -------------------------
        # V1 FALLBACK
        # -------------------------
        forecast = await self.forecast_engine.build(pv, load, price)

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
            "simulation": None,
            "action": "IDLE",
        }

    async def _get_pv_data(self):
        return self.hass.data.get("ems_pv", {})

    async def _get_load_data(self):
        return self.hass.data.get("ems_load", {"avg": 0.5})

    async def _get_price_data(self):
        return self.hass.data.get("ems_price", {"avg": 0.25})
