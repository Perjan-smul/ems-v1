from __future__ import annotations


class DecisionEngine:
    """Basic v2 decision logic (advisory)."""

    def decide(self, forecast, simulation):

        if not simulation:
            return "IDLE"

        pv_now = forecast["pv_kw"][0]
        load_now = forecast["load_kw"][0]
        price_now = forecast["price_eur"][0]

        avg_price = sum(forecast["price_eur"]) / 24

        if pv_now > load_now:
            return "CHARGE"

        if price_now > avg_price:
            return "DISCHARGE"

        return "IDLE"
