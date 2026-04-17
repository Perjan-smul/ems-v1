from __future__ import annotations


class PVLearning:
    """Learns PV forecast correction."""

    def __init__(self, memory):
        self.memory = memory

    def update(self, actual_pv: float, forecast_pv: float):
        error = actual_pv - forecast_pv
        self.memory.add_pv_error(error)

    def correct(self, forecast):
        bias = self.memory.pv_bias()

        return [max(v + bias, 0.0) for v in forecast]
