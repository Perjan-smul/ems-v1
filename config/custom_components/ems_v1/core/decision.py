class DecisionEngine:
    def __init__(self, pv, load, price, battery):
        self.pv = pv
        self.load = load
        self.price = float(price)
        self.battery = battery

    def compute(self):
        if self.price > 0.28 and self.battery.can_discharge():
            return "DISCHARGE"

        if self.pv > self.load and self.battery.can_charge():
            return "CHARGE"

        return "IDLE"