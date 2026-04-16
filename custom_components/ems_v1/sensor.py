from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN]

    entities = [
        EMSActionSensor(coordinator),
        EMSPVSensor(coordinator),
        EMSLoadSensor(coordinator),
        EMSROISensor(coordinator),
    ]

    async_add_entities(entities)


class BaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.coordinator = coordinator


class EMSActionSensor(BaseSensor):
    @property
    def name(self):
        return "EMS Action"

    @property
    def state(self):
        return self.coordinator.data["action"]

    @property
    def icon(self):
        return "mdi:battery"


class EMSPVSensor(BaseSensor):
    @property
    def name(self):
        return "EMS PV Corrected"

    @property
    def state(self):
        return self.coordinator.data["pv_corrected"]

    @property
    def icon(self):
        return "mdi:solar-power"


class EMSLoadSensor(BaseSensor):
    @property
    def name(self):
        return "EMS Load Forecast"

    @property
    def state(self):
        return self.coordinator.data["load_forecast"]

    @property
    def icon(self):
        return "mdi:home-lightning-bolt"


class EMSROISensor(BaseSensor):
    @property
    def name(self):
        return "EMS ROI"

    @property
    def state(self):
        return self.coordinator.data["roi"]

    @property
    def icon(self):
        return "mdi:currency-eur"
