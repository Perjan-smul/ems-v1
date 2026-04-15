from datetime import datetime

class LoadModel:
    def __init__(self, data):
        self.current_load = data["load"]

    def forecast(self):
        # MVP: fallback → current load
        return self.current_load