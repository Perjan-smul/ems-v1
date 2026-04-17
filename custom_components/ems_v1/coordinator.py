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
    """EMS V2 Coordinator with learning pipeline and V1 fallback."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry

        # V2 pipeline (primary)
        self.pipeline = EMSPipeline(hass, entry)

        # V1 fallback
        self.forecast_engine = ForecastEngine(hass, entry)

        super().__init__(
            hass,
            _LOGGER,
            name=f"ems_v2_{entry.entry_id}",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Main update loop."""

        # -------------------------
        # 1. INPUT DATA
        # -------------------------
        pv = await self._get_pv_data()
        load = await self._get_load_data()
        price = await self._get_price_data()

        use_v2 = self.entry.options.get("use_v2_pipeline", True)

        # -------------------------
        # 2. V2 PIPELINE (PRIMARY)
        # -------------------------
        if use_v2:
            try:
                result = await self.pipeline.run(
                    {
                        "pv": pv,
                        "load": load,
                        "price": price,
                        "pv_now": pv["current"],
                        "load_now": load["current"],
                    }
                )

                return {
                    "pv": pv,
                    "load": load,
                    "price": price,
                    "forecast": result.get("forecast"),
                    "simulation": result.get("simulation"),
                    "action": result.get("action"),
                    "learning": result.get("learning"),
                }

            except Exception as e:
                _LOGGER.exception("EMS V2 pipeline failed, falling back to V1: %s", e)

        # -------------------------
        # 3. V1 FALLBACK (SAFE MODE)
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
            "learning": None,
        }

    # ---------------------------------------------------
    # DATA ADAPTERS (CRUCIAAL VOOR STABILITEIT)
    # ---------------------------------------------------

    async def _get_pv_data(self):
        """
        Expected output:
        {
            "current": float,
            "forecast": [24 floats]
        }
        """

        data = self.hass.data.get("ems_pv")

        if isinstance(data, dict):
            return {
                "current": float(data.get("current", 0.0)),
                "forecast": data.get("forecast", [0.0] * 24),
            }

        return {
            "current": 0.0,
            "forecast": [0.0] * 24,
        }

    async def _get_load_data(self):
        """
        Expected output:
        {
            "current": float,
            "forecast": [24 floats]
        }
        """

        data = self.hass.data.get("ems_load")

        if isinstance(data, dict):
            return {
                "current": float(data.get("current", 0.5)),
                "forecast": data.get("forecast", [0.5] * 24),
            }

        return {
            "current": 0.5,
            "forecast": [0.5] * 24,
        }

    async def _get_price_data(self):
        """
        Expected output:
        {
            "forecast": [24 floats]
        }
        """

        data = self.hass.data.get("ems_price")

        if isinstance(data, dict):
            return {
                "forecast": data.get("forecast", [0.25] * 24),
            }

        return {
            "forecast": [0.25] * 24,
        }

    # ---------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------

    async def async_shutdown(self):
        """Cleanup resources if needed."""
        _LOGGER.debug("Shutting down EMS Coordinator")
