class ROICalc:
    def __init__(self, data):
        self.price = float(data["price"])

    def estimate(self, pv, load):
        surplus = max(0, pv - load)
        savings = surplus * self.price

        return {
            "daily": savings,
            "yearly": savings * 365
        }