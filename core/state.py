class EMSState:
    def __init__(self):
        self.soc = 0.0
        self.last_action = "IDLE"
        self.last_prices = []
