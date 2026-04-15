class PVModel:
    def __init__(self, data):
        self.actual = data["pv"]
        self.forecast = data["pv_forecast"]

    def corrected(self):
        if self.forecast <= 0:
            return self.actual

        shadow = self.actual / self.forecast

        # smoothing
        return self.forecast * (0.7 * shadow + 0.3)