from __future__ import annotations


class LoadLearning:
    """Learns load forecast correction."""

    def __init__(self, memory):
        self.memory = memory

    def update(self, actual_load: float, forecast_load: float):
        error = actual_load - forecast_load
        self.memory.add_load_error(error)

    def correct(self, forecast):
        bias = self.memory.load_bias()

        return [max(v + bias, 0.0) for v in forecast]
