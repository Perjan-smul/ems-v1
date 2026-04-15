from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta
from .core.ems_engine import EMSEngine

class EMSCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            logger=None,
            name="ems_v1",
            update_interval=timedelta(seconds=300),
        )

    async def _async_update_data(self):
        data = await self._collect()
        return EMSEngine(data).run()

    async def _collect(self):
        h = self.hass.states

        def get(eid):
            s = h.get(eid)
            try:
                return float(s.state)
            except:
                return 0.0

        return {
            "pv": get("sensor.solaredge_pv_power"),
            "load": get("sensor.p1_power"),
            "price": get("sensor.energy_price"),
            "pv_forecast": get("sensor.pv_forecast"),
            "battery_soc": get("sensor.solaredge_battery_soc"),
        }