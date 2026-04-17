from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ForecastSnapshot:
    pv_kw: List[float]
    load_kw: List[float]
    price_eur: List[float]
    hours: List[int]


class ForecastEngine:
    """Normalizes all input data into 24h forecast vectors."""

    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

    async def build(self, pv_data, load_data, price_data):

        pv = self._normalize_pv(pv_data)
        load = self._normalize_load(load_data)
        price = self._normalize_price(price_data)

        return ForecastSnapshot(
            pv_kw=pv,
            load_kw=load,
            price_eur=price,
            hours=list(range(24)),
        )

    # -------------------------
    # NORMALIZATION
    # -------------------------

    def _normalize_pv(self, pv_data):
        if isinstance(pv_data, dict):
            return pv_data.get("forecast", [0.0] * 24)
        if isinstance(pv_data, list):
            return pv_data
        return [0.0] * 24

    def _normalize_load(self, load_data):
        if isinstance(load_data, dict):
            return load_data.get("forecast", [0.5] * 24)
        if isinstance(load_data, list):
            return load_data
        return [0.5] * 24

    def _normalize_price(self, price_data):
        if isinstance(price_data, dict):
            return price_data.get("forecast", [0.25] * 24)
        if isinstance(price_data, list):
            return price_data
        return [0.25] * 24
