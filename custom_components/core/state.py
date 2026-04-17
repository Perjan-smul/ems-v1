from __future__ import annotations


class EMSState:
    """Runtime state for EMS v2."""

    def __init__(self):
        self.soc = 0.0
        self.last_action = "IDLE"
        self.last_prices = []

    def update(self, decision, forecast):
        self.last_action = decision
        self.last_prices = forecast["price_eur"]
