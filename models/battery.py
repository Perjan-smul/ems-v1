class BatteryModel:
    def __init__(self, data):
        self.soc = data["battery_soc"]

    def can_discharge(self):
        return self.soc > 20

    def can_charge(self):
        return self.soc < 90