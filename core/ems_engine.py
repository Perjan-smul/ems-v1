from ..models.pv import PVModel
from ..models.load import LoadModel
from ..models.battery import BatteryModel
from .decision import DecisionEngine
from .roi import ROICalc

class EMSEngine:
    def __init__(self, data):
        self.data = data

    def run(self):
        pv = PVModel(self.data).corrected()
        load = LoadModel(self.data).forecast()
        battery = BatteryModel(self.data)

        action = DecisionEngine(
            pv, load, self.data["price"], battery
        ).compute()

        roi = ROICalc(self.data).estimate(pv, load)

        return {
            "action": action,
            "pv_corrected": pv,
            "load_forecast": load,
            "roi": roi["yearly"]
        }