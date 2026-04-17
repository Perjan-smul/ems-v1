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
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

    async def build(self, pv_data, load_data, price_data):

        pv = await self._normalize_pv(pv_data)
        load = await self._normalize_load(load_data)
        price = await self._normalize_price(price_data)

        return ForecastSnapshot(
            pv_kw=pv,
            load_kw=load,
            price_eur=price,
            hours=list(range(24)),
        )

    async def _normalize_pv(self, pv_data):
        if not pv_data:
            return [0.0] * 24
        if isinstance(pv_data, list):
            return pv_data
        return [float(pv_data.get("forecast", 0.0))] * 24

    async def _normalize_load(self, load_data):
        if not load_data:
            return [0.5] * 24
        if isinstance(load_data, list):
            return load_data
        base = float(load_data.get("avg", 0.5))
        return [base] * 24

    async def _normalize_price(self, price_data):
        if not price_data:
            return [0.25] * 24
        if isinstance(price_data, list):
            return price_data
        base = float(price_data.get("avg", 0.25))
        return [base] * 24
