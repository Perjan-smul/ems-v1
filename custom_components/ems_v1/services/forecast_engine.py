"""EMS V1.2 Forecast Engine."""

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
    """Normalizes all forecast inputs into 24h aligned vectors."""

    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

    async def build(self, pv_data, load_data, price_data) -> ForecastSnapshot:

        pv = await self._normalize_pv(pv_data)
        load = await self._normalize_load(load_data)
        price = await self._normalize_price(price_data)

        return ForecastSnapshot(
            pv_kw=pv,
            load_kw=load,
            price_eur=price,
            hours=list(range(24)),
        )

    # ---------------- PV ----------------

    async def _normalize_pv(self, pv_data) -> List[float]:
        if not pv_data:
            return [0.0] * 24

        if isinstance(pv_data, list) and len(pv_data) == 24:
            return pv_data

        base = float(pv_data.get("forecast", 0.0))
        return [base] * 24

    # ---------------- LOAD ----------------

    async def _normalize_load(self, load_data) -> List[float]:
        if not load_data:
            return [0.3] * 24

        if isinstance(load_data, list) and len(load_data) == 24:
            return load_data

        base = float(load_data.get("avg", 0.5))

        return [
            base * 0.7, base * 0.6, base * 0.5, base * 0.5,
            base * 0.6, base * 0.8, base * 1.0, base * 1.2,
            base * 1.1, base * 1.0, base * 0.9, base * 0.9,
            base * 1.0, base * 1.1, base * 1.2, base * 1.3,
            base * 1.2, base * 1.0, base * 1.1, base * 1.3,
            base * 1.4, base * 1.2, base * 0.9, base * 0.8,
        ]

    # ---------------- PRICE ----------------

    async def _normalize_price(self, price_data) -> List[float]:
        if not price_data:
            return [0.25] * 24

        if isinstance(price_data, list) and len(price_data) == 24:
            return price_data

        base = float(price_data.get("avg", 0.25))

        return [
            base * 0.8, base * 0.8, base * 0.8, base * 0.8,
            base * 0.9, base * 1.0, base * 1.2, base * 1.4,
            base * 1.3, base * 1.2, base * 1.1, base * 1.0,
            base * 1.0, base * 1.1, base * 1.2, base * 1.4,
            base * 1.5, base * 1.6, base * 1.4, base * 1.2,
            base * 1.1, base * 1.0, base * 0.9, base * 0.8,
        ]
