from __future__ import annotations


class EMSMemory:
    """Simple rolling memory for learning."""

    def __init__(self):
        self.pv_error = []
        self.load_error = []

        self.max_samples = 48  # 2 dagen

    def add_pv_error(self, error: float):
        self.pv_error.append(error)
        if len(self.pv_error) > self.max_samples:
            self.pv_error.pop(0)

    def add_load_error(self, error: float):
        self.load_error.append(error)
        if len(self.load_error) > self.max_samples:
            self.load_error.pop(0)

    def pv_bias(self):
        if not self.pv_error:
            return 0.0
        return sum(self.pv_error) / len(self.pv_error)

    def load_bias(self):
        if not self.load_error:
            return 0.0
        return sum(self.load_error) / len(self.load_error)
