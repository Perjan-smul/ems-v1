from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        EMSSensor(coordinator, "ems_action", "action"),
        EMSSensor(coordinator, "ems_pv_corrected", "pv"),
        EMSSensor(coordinator, "ems_load_forecast", "load"),
        EMSSensor(coordinator, "ems_roi", "simulation"),
    ]

    async_add_entities(entities)


class EMSSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, key):
        super().__init__(coordinator)
        self._attr_name = name
        self._key = key

    @property
    def native_value(self):

        data = self.coordinator.data

        if not data:
            return None

        if self._key == "pv":
            return data.get("forecast", {}).get("pv_kw", [0])[0]

        if self._key == "load":
            return data.get("forecast", {}).get("load_kw", [0])[0]

        if self._key == "simulation":
            sim = data.get("simulation")
            if sim:
                return sim[0]["roi"]  # best scenario
            return None

        if self._key == "action":
            return "IDLE"

        return None
